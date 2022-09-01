from xmlrpc.client import Boolean
from django.db.models import fields
from wagtail.core import models
from wagtail.admin.edit_handlers import (
    # Panels
    FieldPanel,
    HelpPanel,
    MultiFieldPanel,
)

from wagtail_color_panel.fields import ColorField
from wagtail_color_panel.edit_handlers import NativeColorPanel

#-----Page models-----
class SectionablePage(models.Page):
    """
    Abstract class for pages. Allows a page to be aware of which section it belongs to, based on the structure of the site hierarchy. Also contains fields common to any subtree of the site, such as subtree_colour

    Pages in the site heirarchy tend to belong to a section.
    Sections correspond to child nodes of the HomePage that themselves have many children.
    Therefore all SectionablePages have built-in capacity to traverse backwards up the Page tree
    """
    is_creatable = False #no page should ever JUST be a sectionable page. This is an "abstract" page
    current_section = fields.CharField(
        max_length=255, #should contain the SLUG of the current section, not its name. Max length reflects max Wagtail slug length
        null=False,
        blank=True,
        default='',
    )

    colour = ColorField(default="#3490d6")
    apply_colour_to_subtree_when_saved = models.BooleanField(default=False)
    lock_colour = models.BooleanField(default=False)

    settings_panels = models.Page.settings_panels + [
        MultiFieldPanel(
            [
                HelpPanel(
                    content='<p>Colour is intended to be applied to EVERY page that is descendent of a single page at once. This could be <b>extremely</b> slow.</p><p>The application of colours to the descendent pages therefore <b>ONLY</b> occurs when \"Apply colour to subtree when saved\" is checked, and this field will uncheck itself after the save is done.</p><p>"Lock Colour will prevent" any page higher in the hierarchy from modifying colour properties of either this page OR the descendents of this page. If you tried to change the colour of some ancestor node and did not see the change propagate to the descendents, double-check this field.</p>',
                ),
                NativeColorPanel('subtree_colour'),
                FieldPanel('apply_colour_to_subtree_when_saved'),
                FieldPanel('lock_colour'),
            ],
            heading="Advertising-Releated",
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["current_section"] = self.current_section
        return context

    def save(self, *args, **kwargs):
        """
        Several out-the-norm features:

        1. Ensures the page's current section is synced with its parents/ancestors. Or else, if this is a section page, its section is itself.
        2. Can apply colour to all items in subtree
        """


        if self.current_section != self.slug:
            # saves ourselves some queries - the above situation should only ever obtain if we're in a section named after our current page, i.e. at the "Section Root".
            # All the special operations required by a save 

            # TODO: 2022/09/01 - possible code smell? absence of setting of current_section on this page feels a bit noodly
            # I think the rationale was it should go in the SectionPage model because setting it to the slug is supposed to be unique to SectionPages
            ancestors_qs = self.get_ancestors()
            if len(ancestors_qs) == 2:
                # if there are exactly two ancestors (root, homepage), this must be a section page, so use its slug for current section
                # (slightly too magic - if possible improve on this solution - it's hard to know what all and only section pages have without being able to refer to that class!)
                self.current_section = self.slug
            else:
                # otherwise, we have some non-section page that should be able to learn what section it's in from its parent
                try:           
                    self.current_section = ancestors_qs.last().specific.current_section
                except Exception as e:
                    # This shouldn't ever be hit, but worst case scenario the current_section field's use with caching etc. can still work with "ERROR_SECTION"
                    self.current_section = 'ERROR_SECTION'

        if self.apply_colour_to_subtree_when_saved:
            children_qs = self.get_children()

            for child in children_qs:
                if hasattr(child, "lock_colour") and not child.lock_colour:
                    child.apply_colour_to_subtree_when_saved = True
                    child.save()

            self.apply_colour_to_subtree_when_saved = False
            return super().save(*args, **kwargs)    
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True
