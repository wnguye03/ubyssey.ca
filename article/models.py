from . import blocks as article_blocks

from dispatch.models import Article

from django import forms
from django.db import models
from django.db.models.fields import CharField
from django.forms.widgets import Select
from django.utils import timezone

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

@register_snippet
class Topic(models.Model):
    slug = models.SlugField(
        primary_key=True,
        unique=True,
        max_length=255,
        null=False,
        blank=False,
    )
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )
    last_used = models.DateTimeField(
        null=True
    )
    def update_timestamp(self):
        self.last_used = timezone.now()
        self.save()
    
    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"
        indexes = [
            models.Index(fields=['slug']),
        ]

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
        'authors.AuthorSnippet',
        on_delete=models.CASCADE,
    )
    author_role = CharField(        
        # While stored as a CharField, will be selected from a menu. See the Widget in the panels value of this Orderable
        max_length=50,
        null=False,
        blank=True,
        default='',
    )
    panels = [
        MultiFieldPanel(
            [
                SnippetChooserPanel("author"),
                FieldPanel(
                    "author_role",
                    widget=Select(
                        choices=[
                            ('', ''), 
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
    #-----Main attributes-----
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
            ('video', article_blocks.OneOffVideoBlock(
                label = "One Off Video Block",
                template = 'article/stream_blocks/video.html',
                help_text = "Use this for videos that will only be associated with this current article, rather than entered into our video library"
            )),
            ('image', ImageChooserBlock(
                label = "Image"
            )),            
        ],
        null=True,
        blank=True,
    )
    section = models.ForeignKey(
        "SectionSnippet",
        null=True,
        blank=False,
        on_delete=models.PROTECT,
        related_name="+"
    )
    lede = models.TextField(
        # Was called "snippet" in Dispatch - do not want to reuse this work, so we call it 'lede' instead
        null=False,
        blank=True,
        default='',
    )

    #-----Featured Media-----
    
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    featured_video = models.ForeignKey(
        "videos.VideoSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    # importance
    # reading time
    # facebook instant article
    # breaking
    # template

    #-----Promote panel stuff------
    seo_keyword = models.CharField(
        max_length=100, 
        null=False, 
        blank=True, 
        default='',
        verbose_name="SEO Keyword",
    ) # AKA "Focus Keywords" in the old Dispatch frontend
    seo_description = models.TextField(
        null=False,
        blank=True,
        default='',
        verbose_name="SEO Description",
    ) # AKA "Meta Description" in the old Dispatch frontend
    
    #-----Migration stuff------
    dispatch_version = models.ForeignKey(
        # Used to map the article to a previous version that exists in Dispatch
        "dispatch.Article",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    #-----For Wagtail's user interface-----
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                StreamFieldPanel("content"),
            ],
            heading="Article Content",
            help_text = "The main contents of the article, organized into \"blocks\". Most article text should be written in Rich Text Blocks, but many other features are available!",
        ),
        MultiFieldPanel(
            [
                InlinePanel("article_authors", min_num=1, max_num=20, label="Author"),
            ],
            heading="Author(s)",
            help_text="Authors may be created under \"Snippets\", then selected here."
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
                SnippetChooserPanel("featured_video"),
            ],
            heading="Featured Media",
        ),
        MultiFieldPanel(
            [
                FieldPanel("lede")
            ],
            heading="Front Page Stuff",
        ),
    ]
    promote_panels = Page.promote_panels + [
        MultiFieldPanel(
            [
                FieldPanel("seo_keyword"),
                FieldPanel("seo_description"),
            ],
            heading="Old SEO stuff",
            help_text="In Dispatch, \"SEO Keyword\" was referred to as \"Focus Keywords\", and  \"SEO Description\" was referred to as \"Meta Description\""
        )
    ]
    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"