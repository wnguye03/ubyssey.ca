"""
Blocks used on the home page of the site
"""

from wagtail.core import blocks
from django import forms
from dispatch.models import Section

class SectionChooserBlock(blocks.ChooserBlock):
    # based off code from:
    # https://groups.google.com/g/wagtail/c/S26h5GP9_Fk?pli=1
    # maybe move to a different namespace
    target_model = Section
    widget = forms.Select

class HomePageSectionBlock(blocks.StructBlock):
    section = SectionChooserBlock(required=True)

    section.
    class Meta:
        template = "home/home_page_section_block.html"
