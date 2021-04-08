from dispatch.models import Article
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField

# Create your models here.

class ArticlePage(Page):
    template = "article/article_page.html"
    # content = StreamField(
    #     [
    #         ("home_page_section_block",homeblocks.HomePageSectionBlock())
    #     ]
    # )
