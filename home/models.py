from . import blocks as homeblocks

from dispatch.models import Article
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField

# Create your models here.

class HomePage(Page):
    template = "home/home_page.html"
    
    parent_page_types = [
        'wagtailcore.Page',
    ]

    subpage_types = [
        'section.SectionPage',
    ]

    sections_stream = StreamField(
        [
            ("home_page_section_block",homeblocks.HomePageSectionBlock())
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("sections_stream", heading="Sections"),
    ]

    # def get_latest_articles(self):
    #     max_count = 6 # max count for displaying post
    #     return Article.objects.all().order_by('-last_published_at')[:max_count]

    # def get_context(self, request):
    #     context = super().get_context(request)
    #     context['articles'] = self.get_latest_articles()
    #     return context