from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.core import models as wagtail_core_models
from wagtail.core.models import Page


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

    panels = [
        FieldPanel("subsection_name"),
    ]

#-----Page models-----

class SectionPage(wagtail_core_models.Page):
    template = 'section/section.html'
    
    subpage_types = [
        'article.ArticlePage',
        'specialfeaturelanding.SpecialLandingPage',
    ]
    parent_page_type = [
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