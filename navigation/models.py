from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import CharField, URLField
from django.db.models.fields.related import ForeignKey
from django_extensions.db.fields import AutoSlugField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.models import Orderable
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

class NavigationMenuItem(Orderable):

    navigation_menu = ParentalKey(
        "navigation.NavigationMenu",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='navigation_menu_item',
    )
    link_text = CharField(
        max_length=25,
        default='',
        null=False,
        blank=False,
    )
    internal_link = ForeignKey(
        "wagtailcore.Page",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='+'
    )
    external_link = URLField(
        default='',
        null=False,
        blank=True,
    )

    panels = [
        FieldPanel("link_text"),
        MultiFieldPanel([
            PageChooserPanel("internal_link"),
            FieldPanel("external_link"),
        ], heading="Link",
        help_text = "Internal link takes priority over external link. Leave both blank if you want a menu item be non-functional plain text.",
        ),
    ]

#-----Snippet models-----
@register_snippet
class NavigationMenu(ClusterableModel):
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )
    slug = AutoSlugField(
        max_length=100,
        populate_from="name",
        null=False,
        blank=False,
        editable=True,
    )

    panels = [
        MultiFieldPanel([        
            FieldPanel("name"),
            FieldPanel("slug"),
            ], heading="Navigation Menu Essentials",
            help_text = "Identifying information for your menus (e.g. whether this the \"header menu\" or \"footer menu\" etc.)",
        ),
        MultiFieldPanel([
            InlinePanel("navigation_menu_item", min_num=1, max_num=10, label="Menu Item"),
            ], heading="Navigation Menu Links",
            help_text = "Place 'Section' links to facilitate navigation by readers",
        ),
    ]

    def __str__(self):
        return self.name

@register_setting(icon='cogs')
class SitewideMenus(BaseSetting):
    """    
    Collection of the NavigationMenus that are going to be used on many pages.
    Singleton class, and source of truth for the entire site.
    """

    main_header_menu = ForeignKey(
        "navigation.NavigationMenu",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    left_header_menu = ForeignKey(
        "navigation.NavigationMenu",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    right_header_menu = ForeignKey(
        "navigation.NavigationMenu",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    main_footer_menu = ForeignKey(
        "navigation.NavigationMenu",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    second_footer_menu = ForeignKey(
        "navigation.NavigationMenu",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )

    # def save(self, *args, **kwargs):
    #     # Originally from: https://stackoverflow.com/questions/39412968/allow-only-one-instance-of-a-model-in-django
    #     if not self.pk and SitewideMenus.objects.exists():
    #     # if you'll not check for self.pk 
    #     # then error will also raised in update of exists model
    #         raise ValidationError('There is can be only one SitewideMenus instance')
    #     return super(SitewideMenus, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Sitewide Menus"
