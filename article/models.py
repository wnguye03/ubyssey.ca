from . import blocks as article_blocks

from dispatch.models import Article

from django import forms
from django.db import models
from django.db.models.fields import CharField
from django.forms.widgets import Select

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

#-----Snippet Models-----

@register_snippet
class DispatchCounterpartSnippet(models.Model):
    dispatch_version = models.ForeignKey(
        Article,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
    )

@register_snippet
class AuthorSnippet(models.Model):
    slug = models.SlugField(
        primary_key=True,
        unique=True,
        blank=False,
        null=False,
        max_length=255,
    )
    full_name = models.CharField(
        max_length=255,
    )
    # # This implementation represents an "easy" way to implement this which is analogous to how Dispatch did it, though less user-friendly than the alternative
    # image = models.ImageField(
    #     upload_to='images',
    #     null=True,
    #     blank=True,
    # )
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    facebook_url = models.URLField(
        null=True,
        blank=True,
    )
    twitter_url = models.URLField(
        null=True,
        blank=True,
    )
    # For editting in wagtail:
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("slug"),
                FieldPanel("full_name"),
            ],
            heading="Essentials",
        ),
        MultiFieldPanel(
            [
                ImageChooserPanel("image"),
                FieldPanel("title"),
                FieldPanel("facebook_url"),
                FieldPanel("twitter_url"),
            ],
            heading="Optional Stuff",
        ),
    ]

    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

@register_snippet
class SectionSnippet(models.Model):
    slug = models.SlugField(primary_key=True, unique=True, default='news')
    name = models.CharField(max_length=100, unique=True, default='News')

    panels = [
        FieldPanel('slug'),
        FieldPanel('name'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"

#-----Orderable models-----

class ArticleAuthorsOrderable(Orderable):
    """
    This closely corresponds to the Dispatch model that is (mis-)named "Author"
    """
    article_page = ParentalKey(
        "article.ArticlePage",
        related_name="article_authors",
    )
    author = models.ForeignKey(
        'AuthorSnippet',
        on_delete=models.CASCADE,
    )
    author_role = CharField(        
        # While stored as a CharField, will be selected from a menu. See the Widget in the panels value of this Orderable
        max_length=50,
        null=True,
        blank=True,
    )
    panels = [
        MultiFieldPanel(
            [
                SnippetChooserPanel("author"),
                FieldPanel(
                    "author_role",
                    widget=Select(
                        choices=[
                            ('author', 'Author'), 
                            ('illustrator','Illustrator'),
                            ('photographer','Photographer'),
                            ('videographer','Videographer'),
                        ],
                    ),
                ),
            ],
            heading="Author",
        ),
    ]

#-----Page models-----

class ArticlePage(Page):
    template = "article/article_page.html"
    content = StreamField(
        [
            ('richtext', blocks.RichTextBlock(                                
                label="Rich Text Block",
                help_text = "Write your article contents here. See documentation: https://docs.wagtail.io/en/latest/editor_manual/new_pages/creating_body_content.html#rich-text-fields"
            )),
            ('plaintext',blocks.TextBlock(
                label="Plain Text Block",
                help_text = "Warning: Rich Text Blocks preferred! Plain text primarily exists for importing old Dispatch text."
            )),
            ('dropcap', blocks.TextBlock(
                label = "Dropcap Block",
                template = 'article/stream_blocks/dropcap.html',
                help_text = "Create a block where special dropcap styling with be applied to the first letter and the first letter only.\n\nThe contents of this block will be enclosed in a <p class=\"drop-cap\">...</p> element, allowing its targetting for styling.\n\nNo RichText allowed."
            )),
            ('pagebreak', blocks.StaticBlock(
                template = 'article/stream_blocks/pagebreak.html',
                label = "Pagebreak - USE RICHTEXT INSTEAD"
            )),
            ('video', article_blocks.VideoBlock(
                template = 'article/stream_blocks/video.html',
                label = "Video Block",
            )),
            ('image', ImageChooserBlock(
                label = "Image"
            )),
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
        related_name="+"
    )
    # featured_video = models.ForeignKey()
    section = models.ForeignKey(
        "SectionSnippet",
        null=True,
        blank=False,
        on_delete=models.PROTECT,
        related_name="+"
    )
    excerpt = RichTextField(
        # Was called "snippet" in Dispatch - do not want to reuse this work, so we call it 'excerpt' instead
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
        MultiFieldPanel(
            [
                StreamFieldPanel("content"),
            ],
            heading="Article Content",
        ),
        MultiFieldPanel(
            [
                InlinePanel("article_authors", min_num=1, max_num=20, label="Author"),
            ],
            heading="Author(s)"
        ),
        MultiFieldPanel(
            [
                FieldPanel("section"),                
            ],
            heading="Sections and Tags",
        ),
        MultiFieldPanel(
            [
                ImageChooserPanel("featured_image"),                
            ],
            heading="For Front Page",
        ),
    ]

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"