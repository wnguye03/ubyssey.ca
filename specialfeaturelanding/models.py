from . import validators
from . import blocks as specblocks

from dispatch.models import Article
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import StreamField

class SpecialLandingPage(Page):
    """
    This is the general model for "special features" landing pages, such as for the guide, or a magazine.

    It uses weird tricks to be compatible with Dispatch articles 
    """
    template = "specialfeatureslanding/base.html"
    body = StreamField([
        ("dispatch_article", specblocks.DispatchArticleBlock())
        # ("dispatch_article",blocks.CharBlock(help_text="Type the SLUG of an article to be included here", validators=[validators.validate_published_article])),
        ], #end StreamField
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
    ]

    def get_context(self, request, *args, **kwargs):        
        context = super().get_context(request, *args, **kwargs)
        # for i, block in self.body:
        #     print('hello world ' + i)
        #     context['article' + i] = Article.objects.get(is_published=1, slug=block)
        return context
