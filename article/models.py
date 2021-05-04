from dispatch.models import Article
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField

# Create your models here.

class ArticlePage(Page):
    template = "article/article_page.html"
    content = StreamField([
            ('paragraph', blocks.RichTextBlock()),
        ],
        null=True,
        blank=True,
    )
    featured_image = models.ForeignKey(
        # based on https://www.youtube.com/watch?v=KCMdavRBvXE
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+" # for when you're not using any special 
    )
    # featured_video = models.ForeignKey()
    # section = models.ForeignKey()n
    # authors = models.ForeignKey()
    excerpt = RichTextField(
        # Was called "snippet" in Dispatch - do not want to 
        null=True,
        blank=True,
    )
    # importance
    # reading time
    # facebook instant article
    # breaking
    # template
    # SEO focus keywords
    # SEO meta description
    
    dispatch_version = models.ForeignKey(
        # Used to map the article to a previous version that exists in Dispatch
        "dispatch.Article",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
        ImageChooserPanel("featured_image"),
    ]