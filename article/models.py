from dispatch.models import Article
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField

# Create your models here.

class ArticlePage(Page):
    template = "article/article_page.html"
    content = RichTextField()
    featured_image = models.ForeignKey(
        # based on https://www.youtube.com/watch?v=KCMdavRBvXE
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+" # for when you're not using any special 
    )
    # content = StreamField(
    #     [
    #         ("home_page_section_block",homeblocks.HomePageSectionBlock())
    #     ]
    # )

    content_panels = Page.content_panels + [
        FieldPanel("content"),
        ImageChooserPanel("featured_image"),
    ]