"""
Blocks used on the home page of the site
"""
from article.models import ArticlePage

from django import forms
from django.db import models
from dispatch.models import Section

from wagtail.core import blocks
from wagtail.core.blocks import field_block
from wagtail.admin.edit_handlers import PageChooserPanel


class SectionChooserBlock(blocks.ChooserBlock):
    # based off code from:
    # https://groups.google.com/g/wagtail/c/S26h5GP9_Fk?pli=1
    # maybe move to a different namespace
    target_model = Section
    widget = forms.Select

class HomepageFeaturedSectionBlock(blocks.StructBlock):

    section = field_block.PageChooserBlock(
        page_type='section.SectionPage'
    )

    layout = blocks.ChoiceBlock(
        choices=[
            ('news', '\"News Section" Style'),
            ('featured', '\"Featured Section\" Style'),
        ],
        default='news',
        required=True,
    )

    def get_context(self, value, parent_context=None):
        # When working with a model it's often not a good idea to make a bunch of context variables like this,
        # because most values are simply attributes of the model and we can just pass the model object to the context
        # Becuase a block isn't a model, Django's templating can get confused by the relatively complex data structures involved.
        # Therefore for ease of use, we make sure the values we want to use in templates are visible in context here.

        context = super().get_context(value, parent_context=parent_context)
        context['section'] = value['section']
        context['layout'] = value['layout']
        context['articles'] = context['section'].get_featured_articles()          
        return context

    class Meta:
        template = "home/stream_blocks/section_block.html"

class AboveCutBlock(blocks.StructBlock):
    # Ideally this will be used to grant the user more control of what happens "above the cut"
    # As of 2022/05/18, all it does is expose to the user what was previously just implemented with a hardcoded "include"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        qs = ArticlePage.objects.live().public.order_by('explicit_published_at')
        context['articles'] = qs[:6]
        return context

    class Meta:
        template = "home/stream_blocks/above_cut_block.html"