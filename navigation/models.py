import re
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db import models
from django.db.models.fields import CharField, URLField
from django.db.models.fields.related import ForeignKey
from django_extensions.db.fields import AutoSlugField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from section.models import SectionPage
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, HelpPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.models import Orderable
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

class NavigationMenuOrderable(Orderable):
    """
    Abstract class for DRY implementation of different menus
    Useage: implement ParentalKey on a case-by-case basis
    """

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
    def link(self) -> str:
        if self.internal_link:
            return self.internal_link.url
        elif self.external_link:
            return self.external_link
        else:
            return '#'

    @property
    def text(self) -> str:
        if self.internal_link and self.link_text == '':
            return self.internal_link.title
        elif self.link_text != '':
            return self.link_text
        else:
            return "ERROR MISSING LINK TEXT"


    @property
    def internal_link_slug(self) -> str:
        if self.internal_link:
            return self.internal_link.slug
        else:
            return "ERROR-NOT-AN-INTERNAL-LINK"
    
    # @classmethod
    # def class_cache_name(cls):
    #     """
    #     An entire menu is cached as a template fragment, so if any single orderable in that menu is changed, we need to flush the cache.
    #     Since a menu is just a bundle of orderables, we associate the cache name with the orderables' class.
    #     Uses regex to trim string to avoid "CacheKeyWarning: Cache key contains characters that will cause errors if used with memcached"
    #     A little more complex than ideal.
    #     """
    #     result = re.search('\'(.*)\'', str(cls))
    #     s = result.group(1)
    #     return '%s-cache' % s

    # def save(self, **kwargs):
    #     class_cache_name = type(self).class_cache_name()
    #     print(class_cache_name)
    #     key = make_template_fragment_key(class_cache_name)
    #     print(key)
    #     print(cache.get(key))
    #     cache.delete(key) 
    #     return super().save(**kwargs)

    # class Meta:
    #     abstract = True


class MainHeaderNavigationItem(NavigationMenuOrderable):
    navigation_menu = ParentalKey(
        "navigation.SitewideMenus",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='main_header_menu',
    )
class LeftHeaderNavigationItem(NavigationMenuOrderable):
    navigation_menu = ParentalKey(
        "navigation.SitewideMenus",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='left_header_menu',
    )
class RightHeaderNavigationItem(NavigationMenuOrderable):
    navigation_menu = ParentalKey(
        "navigation.SitewideMenus",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='right_header_menu',
    )
class MainFooterNavigationItem(NavigationMenuOrderable):
    navigation_menu = ParentalKey(
        "navigation.SitewideMenus",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='main_footer_menu',
    )
class SecondFooterNavigationItem(NavigationMenuOrderable):
    navigation_menu = ParentalKey(
        "navigation.SitewideMenus",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='second_footer_menu',
    )
class MobileLinksNavigationItem(NavigationMenuOrderable):
    navigation_menu = ParentalKey(
        "navigation.SitewideMenus",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='mobile_links_menu',
    )

#-----Settings models-----

@register_setting(icon='cogs')
class SitewideMenus(ClusterableModel, BaseSetting):
    """    
    Collection of the NavigationMenus that are going to be used on many pages.
    Singleton class, and source of truth for the entire site.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.CACHES = (
            'left_header',
            'right_header',
            'main_header',
            'main_footer',
            'secondary_footer',
        ) # these correspond to the template fragment names
        
    panels = [
        HelpPanel(
            content="<p>Use this to select menus to be used as the main interface for navigating our website.</p><p>CAUTION: These settings are very important! You should not clear, choose another, or edit these menus unless headers or footers on the site look incorrect.</p>",
            heading="Help"
        ),
        MultiFieldPanel([        
            InlinePanel("main_header_menu"),
            ], heading="Main Header",
            help_text="Will appear in header of every page of the site, in header, or in special menu on mobile",
        ),
        MultiFieldPanel([        
            InlinePanel("left_header_menu"),
            ], heading="Left Secondary Header",
            help_text="Mostly will only be seen on the homepage of the site.",
        ),
        MultiFieldPanel([        
            InlinePanel("right_header_menu"),
            ], heading="Right Secondary Header",
            help_text="Mostly will only be seen on the homepage of the site.",
        ),
        MultiFieldPanel([        
            InlinePanel("main_footer_menu"),
            ], heading="Footer",
            help_text="Will appear in footer of every page of the site.",
        ),
        MultiFieldPanel([                
            InlinePanel("second_footer_menu"),
            ], heading="Footer Second Row",
            help_text="Will appear in footer of every page of the site.",
        ),

        MultiFieldPanel([        
            InlinePanel("mobile_links_menu"),
            ], heading="Mobile \"Links\" Menu",
            help_text="Links that will appear in the mobile menu alongside the main header links",
        ),
    ]
    # def save(self, **kwargs):
    #     for cache_name in self.CACHES:
    #         key = make_template_fragment_key(cache_name)
    #         cache.delete(key) 
    #     return super().save(**kwargs)

    class Meta:
        verbose_name = "Site-Wide Menus"
        verbose_name_plural = "Instances of \'Site-Wide Menus\'"
