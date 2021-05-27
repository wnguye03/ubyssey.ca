from django.db import models
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.core import models as wagtail_core_models
from wagtail.core.models import Page
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

#-----Snippet models-----
@register_snippet
class SubsectionSnippet(models.Model):
    name = models.CharField(
        max_length=100,
    )
    slug = models.CharField(
        max_length=100,
    )

#-----Orderable models-----
class SubsectionsOrderable(wagtail_core_models.Orderable):
    """
    This closely corresponds to the Dispatch model that is (mis-)named "Author"
    """
    section_page = ParentalKey(
        "section.SectionPage",
        related_name="subsections",
    )
    subsection_name = models.CharField(
        max_length=100,
    )
    subsection_snippet = ForeignKey(
        'section.SubsectionSnippet',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    panels = [
        FieldPanel("subsection_name"),
        MultiFieldPanel(
        [
            SnippetChooserPanel("subsection_snippet"),
        ]),      
    ]

#-----Page models-----

class SectionPage(wagtail_core_models.Page):
    template = 'section/section_page.html'

    subpage_types = [
        'article.ArticlePage',
        'specialfeaturelanding.SpecialLandingPage',
    ]
    parent_page_types = [
        'home.HomePage',
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                InlinePanel("subsections"),
            ],
            heading="Subsection(s)",
        ),
    ]