from django.db import models
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList, InlinePanel, MultiFieldPanel, HelpPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.models import Orderable

from wagtailmodelchooser import register_model_chooser
from wagtailmodelchooser.edit_handlers import ModelChooserPanel

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

@register_model_chooser
class AdSlot(models.Model):
    """
    About:
        Definition of "ad slot" according to Google Ad Manager glossary:

            "An ad slot is the HTML markup (usually between <div> tags) the defines where an ad appears.
            Ad slots can reference either unique ad units or, if on a single page, ad slots can also reference the same ad unit."

        (from https://support.google.com/admanager/table/7636513?hl=en, accessed 2022/05/26)

        This class models the data that distinguishes different ad slots in the HTML.
        It works with the template tag "adslot" to insert these HTML elements into templates.

        The relevant divs for displaying ads will be selected by the class, which
        should be a fixed part of the template used to render this information.
        This, unlike the rest of the attributes used to construct the relevant div
        should NOT having a corresponding field in this model, because it is constant and not variable.
        
        To use an ad slot to display an ad, use the Google Publisher Tag library to call googletag.defineSlot
        https://developers.google.com/publisher-tag/reference#googletag.defineSlot 

    Attributes:
        slug: identifies entry in table
        size: str - dfp.js keeps a dictionary of standard ad sizes. The possible choices for this field represent the keys for that dictionary.
        div_id: str - "id" in the sense of an HTML attribute. 
        dfp: str - Corresponds to the ad unit on the Google Ad Manager side of things.
        template: template used to render this information. Only one such template exists by default. 
    """
    slug = models.SlugField(null=False, blank=False, unique=True)
    div_id = models.CharField(null=False, blank=True, default='', max_length=255, verbose_name="HTML Element ID")
    size = models.CharField(null=False, blank=False, default='box', max_length=255,
        choices=[
            ('box','Box'),
            ('skyscraper', 'SkyScraper'),
            ('banner','Banner'),
            ('leaderboard',"Leaderboard"),
            ('mobile-leaderboard',"Mobile Leaderboard"),
        ],
    )
    dfp = models.CharField(null=False, blank=True, default='', max_length=255, verbose_name="Ad Unit Name")
    div_class = models.CharField(null=False, blank=True, default='box', max_length=255,
        choices=[
            ('','Default'),
            ('homepage', 'Homepage'),
            ('mobile-frontpage-box', 'Mobile Frontpage Box'),            
        ],
    )

    def __str__(self) -> str:
        return self.slug

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['slug']),
        ]

@register_setting(icon='cogs')
class AdSettings(BaseSetting):
    
    #-----Appear on Section Page only-----
    leaderboard_ad_slot = models.ForeignKey(
        AdSlot,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    mobile_leaderboard_ad_slot = models.ForeignKey(
        AdSlot,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    #-----Appear on Article Page only-----
    article_right_column_skyscraper_ad_slot = models.ForeignKey(
        AdSlot,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    article_right_column_boxA_ad_slot = models.ForeignKey(
        AdSlot,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    article_right_column_boxB_ad_slot = models.ForeignKey(
        AdSlot,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    #-----Editor interface-----
    section_ad_panels = [
        ModelChooserPanel('leaderboard_ad_slot'),
        ModelChooserPanel('mobile_leaderboard_ad_slot'),
    ]
    article_ad_panels = [
        ModelChooserPanel('article_right_column_skyscraper_ad_slot'),
        ModelChooserPanel('article_right_column_boxA_ad_slot'),
        ModelChooserPanel('article_right_column_boxB_ad_slot'),
    ]
    edit_handler = TabbedInterface([
        ObjectList(section_ad_panels, heading='Section Page Ads'),
        ObjectList(article_ad_panels, heading='Article Page Ads'),
    ])
    class Meta:
        verbose_name = "Side-Wide Ad Slots"
        verbose_name_plural = "Instances of \Side-Wide Ad Slots\'"

@register_setting(icon='cogs')
class AdTagSettings(ClusterableModel, BaseSetting):
    # There should be one of these per (major) page type:
    # Home Page, Section Page, Article Page
    panels = [
        MultiFieldPanel(
            [
                HelpPanel(content='This is where the explanation on how to add Google Ad Manager ads to our website go.\nThere are two tags per ad slot: a "head" tag which communicates with Google, and a "placement" tag')
            ],
            heading="How to add Google Ad Manager ads to the site"
        ),
        MultiFieldPanel(
            [
                InlinePanel("ad_head_orderables", label="Ad Head Tags"),
            ],
            heading="Ad Head Tags"
        ),
        MultiFieldPanel(
            [
                InlinePanel("ad_placement_orderables", label="Ad Placement Tags"),
            ],
            heading="Ad Placement Tags"
        ),
    ]

class AdHeadOrderable(Orderable):
    ad_slot = models.ForeignKey(
        AdSlot,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name="Ad Slot"
    )
    settings = ParentalKey(AdTagSettings,related_name='ad_head_orderables')

    panels = [
        ModelChooserPanel('ad_slot'),
    ]


class AdPlacementOrderable(Orderable):
    ad_slot = models.ForeignKey(
        AdSlot,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name="Ad Slot"
    )
    settings = ParentalKey(AdTagSettings,related_name='ad_placement_orderables')

    panels = [
        ModelChooserPanel('ad_slot'),
    ]
