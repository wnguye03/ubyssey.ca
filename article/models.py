import datetime

from dispatch.models import Article

from django.db import models
from django.db.models.fields import CharField
from django.forms.widgets import Select
from django.utils import timezone

from itertools import groupby
from django.utils.functional import empty

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from section.sectionable.models import SectionablePage

from taggit.models import TaggedItemBase

from videos import blocks as video_blocks

from wagtail.admin.edit_handlers import (
    FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel,
)
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet


UBYSSEY_FOUNDING_DATE = datetime.date(1918,10,17)

#-----Snippet Models-----

@register_snippet
class DispatchCounterpartSnippet(models.Model):
    dispatch_version = models.ForeignKey(
        Article,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
    )


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
        'authors.AuthorPage',
        on_delete=models.CASCADE,
        related_name="article_authors",
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
                PageChooserPanel("author"),
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

class ArticleFeaturedMediaOrderable(Orderable):
    """
    This is based off the "ImageAttachment" class from Dispatch

    The ImageAttachment class was a bit of an oddity but it was clear that it was supposed to be an "intermediary"
    between an article and an image model in a very analogous way to Orderables, even having an apparently unused
    "Orderable" field.

    Because essentialy identical classes were used for both Images and Videos, we are here making code more DRY
    for an article
    """
    article_page = ParentalKey(
        "article.ArticlePage",
        related_name="featured_media",
    )

    caption = models.TextField(blank=True, null=False, default='')
    credit = models.TextField(blank=True, null=False, default='')
    # style = models.CharField(max_length=255, blank=True, null=False, default='')
    # width = models.CharField(max_length=255, blank=True, null=False, default='')
    image = models.ForeignKey(
        "images.UbysseyImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    video = models.ForeignKey(
        "videos.VideoSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        MultiFieldPanel(
            [
                ImageChooserPanel("image"),
                SnippetChooserPanel("video"),
            ],
            heading="Media Choosers",
        ),
        MultiFieldPanel(
            [
                FieldPanel("caption"),
                FieldPanel("credit"),
            ],
            heading="Caption/Credits",
        ),
    ]


#-----Taggit models-----
class ArticlePageTag(TaggedItemBase):
    """
    Reference: 
    https://docs.wagtail.io/en/stable/reference/pages/model_recipes.html
    """
    content_object = ParentalKey('article.ArticlePage', on_delete=models.CASCADE, related_name='tagged_items')
    class Meta:
        verbose_name = "article tag"
        verbose_name_plural = "article tags"

#-----Page models-----

class ArticlePage(SectionablePage):
    #-----Main attributes-----
    template = "article/article_page.html"

    parent_page_types = [
        'specialfeaturelanding.SpecialLandingPage',
        'section.SectionPage',
    ]

    subpage_types = [] #Prevents article pages from having child pages

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
            ('video', video_blocks.OneOffVideoBlock(
                label = "Credited/Captioned One-Off Video",
                help_text = "Use this to credit or caption videos that will only be associated with this current article, rather than entered into our video library. You can also embed videos in a Rich Text Block."
            )),
            ('image', ImageChooserBlock(
                label = "Image"
            )),
            ('raw_html', blocks.RawHTMLBlock(
                label = "Raw HTML Block",
                help_text = "WARNING: DO NOT use this unless you really know what you're doing!"
            )),            
        ],
        null=True,
        blank=True,
    )
    explicit_published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Published At (Override)",
        help_text = "Optional. Publication date which is explicitly shown to the reader. Articles are seperately date/timestamped for database use; if this field is blank front page etc. will display the database publication date.",
    )
    last_modified_at = models.DateTimeField(
        # updates to current date/time every time the model's .save() method is hit
        auto_now=True,
    )
    show_last_modified = models.BooleanField(
        default = False,
        help_text = "Check this to alert readers the article has been revised since its publication.",
    )
    lede = models.TextField(
        # Was called "snippet" in Dispatch - do not want to reuse this work, so we call it 'lede' instead
        null=False,
        blank=True,
        default='',
    )

    #-----Category and Tag stuff-----
    category = models.ForeignKey(
        "section.CategorySnippet",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    tags = ClusterTaggableManager(through='article.ArticlePageTag', blank=True)

    #-----Featured Media-----
    
    featured_video = models.ForeignKey(
        "videos.VideoSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    # template

    #-----Promote panel stuff------
    is_breaking = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name="Breaking News?",
    )
    breaking_timeout = models.DateTimeField(
        # Note: should appear on interface contingent on "is breaking" being checked. Defaults are to ensure functionality prior to implementing this
        null=False,
        blank=False,
        default=timezone.now,
    )
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
    #-----Setting panel stuff-----
    is_explicit = models.BooleanField(
        default=False,
        verbose_name="Is Explicit?",
        help_text = "Check if this article contains advertiser-unfriendly content. Disables ads for this specific article."
    )
    #-----Migration stuff------
    dispatch_version = models.ForeignKey(
        # Used to map the article to a previous version that exists in Dispatch
        "dispatch.Article",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    #-----Hidden stuff: editors don't get to modify these, but they may be programatically changed-----
    revision_id = models.PositiveIntegerField(
        null=False,
        blank=False,
        default=0,
    )
    created_at_time = models.DateTimeField(
        null=False,
        blank=False,
        default=timezone.now,
    )
    legacy_revised_at_time = models.DateTimeField(
        null=False,
        blank=False,
        default=timezone.now,
    )
    legacy_published_at_time = models.DateTimeField(
        null=True,
        default=datetime.datetime.combine(UBYSSEY_FOUNDING_DATE, datetime.time())
    )

    #-----For Wagtail's user interface-----
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                StreamFieldPanel("content"),
            ],
            heading="Article Content",
            help_text = "The main contents of the article are organized into \"blocks\". Click the + to add a block. Most article text should be written in Rich Text Blocks, but many other features are available!",
        ),
        MultiFieldPanel(
            [
                InlinePanel("article_authors", min_num=1, max_num=20, label="Author"),
            ],
            heading="Author(s)",
            help_text="Authors may be created under \"Snippets\", then selected here."
        ),
        FieldRowPanel(
            [
                FieldPanel("explicit_published_at"),
                FieldPanel("show_last_modified"),
            ],
            heading="Publication Date"
        ),
        MultiFieldPanel(
            [
                # FieldPanel("section"),
                SnippetChooserPanel("category"),
                FieldPanel("tags"),
            ],
            heading="Sections and Tags",
        ),
        MultiFieldPanel(
            [
                InlinePanel("featured_media", label="Featured Image or Video"),
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
                FieldPanel("is_breaking"),
                FieldPanel("breaking_timeout"),
            ],
            heading="Old SEO stuff",
            help_text="\"Breaking Timeout\" is irrelevant if news is not breaking news."
        ),
        MultiFieldPanel(
            [
                FieldPanel("seo_keyword"),
                FieldPanel("seo_description"),
            ],
            heading="Old SEO stuff",
            help_text="In Dispatch, \"SEO Keyword\" was referred to as \"Focus Keywords\", and  \"SEO Description\" was referred to as \"Meta Description\""
        )
    ]

    settings_panels = Page.settings_panels + [
        MultiFieldPanel(
            [
                FieldPanel(
                    'is_explicit',
                    help_text = "Check if this article contains advertiser-unfriendly content. Disables ads for this specific article.",
                ),
            ],
            heading="Advertising-Releated",
        ),
    ]

    #-----Properties, getters, setters, etc.-----

    def get_authors_string(self, links=False, authors_list=[]) -> str:
        """
        Returns html-friendly list of the ArticlePage's authors as a comma-separated string (with 'and' before last author).
        Keeps large amounts of logic out of templates.

          links: Whether the author names link to their respective pages.
        """
        def format_author(article_author):
            if links:
                return '<a href="%s">%s</a>' % (article_author.author.full_url, article_author.author.full_name)
            return article_author.author.full_name

        if not authors_list:
            authors = list(map(format_author, self.article_authors.all()))
        else:
            authors = list(map(format_author, authors_list))

        if not authors:
            return ""
        elif len(authors) == 1:
            # If this is the only author, just return author name
            return authors[0]

        return ", ".join(authors[0:-1]) + " and " + authors[-1]        
    authors_string = property(fget=get_authors_string)

    def get_authors_with_urls(self) -> str:
        """
        Wrapper for get_authors_string for easy use in templates.
        """
        return self.get_authors_string(links=True)
    authors_with_urls = property(fget=get_authors_with_urls)

    def get_authors_with_roles(self) -> str:
        """Returns list of authors as a comma-separated string
        sorted by author type (with 'and' before last author)."""

        authors_with_roles = ''
        string_written = ''
        string_photos = ''
        string_author = ''
        string_videos = ''

        authors = dict((k, list(v)) for k, v in groupby(self.article_authors.all(), lambda a: a.author_role))
        for author in authors:
            if author == 'author':
                string_written += 'Written by ' + self.get_authors_string(links=True, authors_list=authors['author'])
            if author == 'photographer':
                string_photos += 'Photos by ' + self.get_authors_string(links=True, authors_list=authors['photographer'])
            if author == 'illustrator':
                string_author += 'Illustrations by ' + self.get_authors_string(links=True, authors_list=authors['illustrator'])
            if author == 'videographer':
                string_videos += 'Videos by ' + self.get_authors_string(links=True, authors_list=authors['videographer'])
        if string_written != '':
            authors_with_roles += string_written
        if string_photos != '':
            authors_with_roles += ', ' + string_photos
        if string_author != '':
            authors_with_roles += ', ' + string_author
        if string_videos != '':
            authors_with_roles += ', ' + string_videos
        return authors_with_roles
    authors_with_roles = property(fget=get_authors_with_roles)
 
    @property
    def published_at(self):
        if self.explicit_published_at:
            return self.explicit_published_at
        return self.first_published_at

    class Meta:
        # TODO Should probably index on:
        # Author then article
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        indexes = [
            models.Index(fields=['category',]),
        ]
