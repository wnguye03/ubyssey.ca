from django.db import models
from django.db.models.fields import CharField, URLField
from django.db.models.fields.related import ForeignKey
from django_extensions.db.fields import AutoSlugField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, HelpPanel
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
        related_name='navigation_menu_items',
    )
    link_text = CharField(
        max_length=25,
        default='',
        null=False,
        blank=True,
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
        ),
        HelpPanel(content="Internal link takes priority over external link."),
    ]

    @property
    def link(self):
        if self.internal_link:
            return self.internal_link.url
        elif self.external_link:
            return self.external_link
        else:
            return '#'

    @property
    def text(self):
        if self.internal_link and self.link_text == '':
            return self.internal_link.title
        elif self.link_text != '':
            return self.link_text
        else:
            return "MISSING LINK TEXT"
        

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
        HelpPanel(
            content="<p>Navigation Menus contain an ordered collection of links.</p><p>The most common use of them is to render the menus use use to navigate the website. Because rendering is different in different situations, there is no standard template used for Navigation Menus; they are implemented differently in different Page templates.</p>",
            heading="Help"
        ),
        MultiFieldPanel([        
            FieldPanel("name"),
            FieldPanel("slug"),
            ], heading="Navigation Menu Essentials",
            help_text = "Identifying information for your menus (e.g. whether this the \"header menu\" or \"footer menu\" etc.)",
        ),
        MultiFieldPanel([
            InlinePanel("navigation_menu_items", min_num=1, max_num=10, label="Menu Item"),
            ], heading="Navigation Menu Links",
            help_text = "Choose links to facilitate navigation by readers.",
        ),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Navigation Menu"
        verbose_name_plural = "Navigation Menus"

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
        related_name='+',
    )
    left_header_menu = ForeignKey(
        "navigation.NavigationMenu",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
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

    panels = [
        HelpPanel(
            content="<p>Use this to select menus to be used as the main interface for navigating our website.</p><p>CAUTION: These settings are very important! You should not clear, choose another, or edit these menus unless headers or footers on the site look incorrect.</p>",
            heading="Help"
        ),
        MultiFieldPanel([        
            SnippetChooserPanel("main_header_menu"),
            ], heading="Main Header",
            help_text="Will appear in header of every page of the site, in header",
        ),
        MultiFieldPanel([        
            SnippetChooserPanel("left_header_menu"),
            SnippetChooserPanel("right_header_menu"),
            ], heading="Secondary Header",
            help_text="Mostly will only be seen on the homepage of the site.",
        ),
        MultiFieldPanel([        
            SnippetChooserPanel("main_footer_menu"),
            SnippetChooserPanel("second_footer_menu"),
            ], heading="Footer",
            help_text="Will appear in header of every page of the site, in footer. Each selected menu represents a different row.",
        ),

    ]


    class Meta:
        verbose_name = "Site-Wide Menus"
        verbose_name_plural = "Instances of \'Site-Wide Menus\'"
