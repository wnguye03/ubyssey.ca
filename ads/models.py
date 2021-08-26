from django.db import models

# Create your models here.


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

    Slots need three pieces of information. Below information Information taken from 

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
    template = models.CharField(null=False, blank=False, default='ads/advertisement.html', max_length=255,
        choices=[
            ('ads/advertisement.html','ads/advertisement.html'),
        ],
    )

    def __str__(self) -> str:
        return self.slug