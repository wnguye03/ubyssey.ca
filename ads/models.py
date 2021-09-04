from django.db import models
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtailmodelchooser import register_model_chooser
from wagtailmodelchooser.edit_handlers import ModelChooserPanel

@register_model_chooser
class AdSlot(models.Model):
    """
    Corresponds to the data needed for frontend scripts that will render ads.
    Works clsoely with ubyssey/js/dfp.js

    "DFP" stands for "DoubleClick for Publishers", the features of which have been rolled
    into Google Ad Manager as of this writing (2021)

    The relevant divs for displaying ads will be selected by the class, which
    should be a fixed part of the template used to render this information.
    This, unlike the rest of the attributes used to construct the relevant div
    should NOT having a corresponding field in this model, because it is constant and not variable.
    
    The ultimate goal of these fields is to allow the Google Publisher Tag library to call googletag.defineSlot in dfp.js
    https://developers.google.com/publisher-tag/reference#googletag.defineSlot 

    Attributes:
        slug: identifies entry in table
        size: str - dfp.js keeps a dictionary of standard ad sizes. The possible choices for this field represent the keys for that dictionary.
        div_id: str - "id" in the sense of a div attribute. 
        dfp: str - Corresponds to the ad unit on the Google Ad Manager side of things.
        template: template used to render this information. Only one such template exists by default. 
    """
    slug = models.SlugField(null=False, blank=False, unique=True)
    div_id = models.CharField(null=False, blank=True, default='', max_length=255)
    size = models.CharField(null=False, blank=False, default='box', max_length=255,
        choices=[
            ('box','Box'),
            ('skyscraper', 'SkyScraper'),
            ('banner','Banner'),
            ('leaderboard',"Leaderboard"),
            ('mobile-leaderboard',"Mobile Leaderboard"),
        ],
    )
    dfp = models.CharField(null=False, blank=True, default='', max_length=255)
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