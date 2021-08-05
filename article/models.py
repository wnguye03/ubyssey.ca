import datetime

from wagtail.admin import edit_handlers
from images.models import GallerySnippet

from dbtemplates.models import Template as DBTemplate

from dispatch.models import Article

from django.db import models
from django.db.models import fields
from django.db.models.fields import CharField
from django.db.models.query import QuerySet
from django.forms.widgets import Select
from django.utils import timezone

from itertools import groupby
from images import blocks as image_blocks
from images.models import GallerySnippet

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from modelcluster.contrib.taggit import ClusterTaggableManager

from section.sectionable.models import SectionablePage

from taggit.models import TaggedItemBase

from videos import blocks as video_blocks

from wagtail.admin.edit_handlers import (
    # Panels
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel, 
    StreamFieldPanel,
    # Custom admin tabs
    ObjectList,
    TabbedInterface,
)
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, PageManager, Orderable
from wagtail.documents.models import Document
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from wagtailmodelchooser.edit_handlers import ModelChooserPanel


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

@register_snippet
class ArticleSeriesSnippet(ClusterableModel):
    title = fields.CharField(
        blank=False,
        null=False,
        max_length=200
    )
    slug = fields.SlugField(
        unique=True,
        blank=False,
        null=False,
        max_length=200
    )
    panels = [
        MultiFieldPanel(
            [
                FieldPanel('title'),
                FieldPanel('slug'),
            ],
            heading="Essentials"
        ),
        MultiFieldPanel(
            [
                InlinePanel("articles", label="Articles"),
            ],
            heading="articles"
        ),
    ]
    def __str__(self):
        return self.title
    class Meta:
         verbose_name = "Series of Articles"
         verbose_name_plural = "Series of Articles"

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

class SeriesOrderable(Orderable):
    """
    Represents a single article in a series of articles. Associated with ArticleSeriesSnippet
    """
    article = models.ForeignKey(
        "article.ArticlePage",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="+",
    )
    series = ParentalKey(
        "ArticleSeriesSnippet",
        default='',
        related_name="articles",
    )
    panels = [
        MultiFieldPanel(
            [
                PageChooserPanel('article'),
            ],
            heading="Article"
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

class ArticleStyleOrderable(Orderable):
    css = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='+',
    )
    article_page = ParentalKey(
        "article.ArticlePage",
        related_name="styles",
    )
    panels = [
        MultiFieldPanel(
            [
                DocumentChooserPanel('css'),
            ],
            heading="CSS Document"
        ),
    ]

class ArticleScriptOrderable(Orderable):
    script = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='+',
    )
    article_page = ParentalKey(
        "article.ArticlePage",
        related_name="scripts",
    )
    panels = [
        MultiFieldPanel(
            [
                DocumentChooserPanel('script'),
            ],
            heading="Script"
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

#-----Manager models-----
class ArticlePageManager(PageManager):
    
    def from_section(self, section_slug='', section_root=None) -> QuerySet:
        from .models import ArticlePage
        if section_slug:
            try:
                new_section_root = Page.objects.get(slug=section_slug)
            except Page.DoesNotExist:
                new_section_root = None
            if new_section_root:
                section_root = new_section_root
            
        return self.live().public().descendant_of(section_root).exact_type(ArticlePage) #.order_by('-last_modified_at')

#-----Page models-----

class ArticlePage(SectionablePage):

    #-----Django/Wagtail settings etc-----
    objects = ArticlePageManager()

    parent_page_types = [
        'specialfeaturelanding.SpecialLandingPage',
        'section.SectionPage',
    ]

    subpage_types = [] #Prevents article pages from having child pages

    #-----Field attributes-----
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
                help_text = "DO NOT USE - Legacy block. Create a block where special dropcap styling with be applied to the first letter and the first letter only.\n\nThe contents of this block will be enclosed in a <p class=\"drop-cap\">...</p> element, allowing its targetting for styling.\n\nNo RichText allowed."
            )),
            ('video', video_blocks.OneOffVideoBlock(
                label = "Credited/Captioned One-Off Video",
                help_text = "Use this to credit or caption videos that will only be associated with this current article, rather than entered into our video library. You can also embed videos in a Rich Text Block."
            )),
            ('image', image_blocks.ImageBlock(
            )),
            ('raw_html', blocks.RawHTMLBlock(
                label = "Raw HTML Block",
                help_text = "WARNING: DO NOT use this unless you really know what you're doing!"
            )),
            ('quote', blocks.StructBlock(
                [
                    ('content',blocks.CharBlock(required=False)),
                    ('source',blocks.CharBlock(required=False)),
                ],
                label = "Pull Quote",
                template = 'article/stream_blocks/quote.html',
            )),
            ('gallery', SnippetChooserBlock(
                target_model = GallerySnippet,
                template = 'article/stream_blocks/gallery.html',
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

    # template #TODO

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

    legacy_template = models.CharField(
        null=False,
        blank=True,
        default='',
        max_length=3000,
    )
    legacy_template_data = models.TextField(
        null=False,
        blank=True,
        default='',
    )
    legacy_revision_number = models.IntegerField(
        default=0
    )

    #-----Custom layout etc-----
    use_default_template = models.BooleanField(default=True)

    db_template = models.ForeignKey(
        DBTemplate,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',        
    )

    def get_template(self, request):
        if not self.use_default_template:
            if self.db_template:
                return self.db_template.name
        return "article/article_page.html"

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
                FieldPanel("lede")
            ],
            heading="Front Page Stuff",
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
        MultiFieldPanel(
            [
                FieldPanel(
                    'legacy_revision_number',
                    help_text = "DO NOT TOUCH",
                ),
            ],
            heading='Legacy stuff'
        ),
    ]

    customization_panels = [
        MultiFieldPanel(
            [
                FieldPanel("use_default_template"),
                ModelChooserPanel("db_template"),
            ],
            heading="Custom HTML",
        ),
        MultiFieldPanel(
            [
                InlinePanel("styles"),
            ],
            heading="Custom CSS",
            help_text="Please upload any custom CSS to \"Documents\", then select the appropriate document here.\n\nSelecting a non-CSS Document will cause errors.",
        ),
        MultiFieldPanel(
            [
                InlinePanel("scripts"),
            ],
            heading="Custom JavaScript",
            help_text="Please upload any custom JavaScript to \"Documents\", then select the appropriate document here.\n\nSelecting a non-JavaScript Document will cause errors.",
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading='Content'),
            ObjectList(promote_panels, heading='Promote'),
            ObjectList(settings_panels, heading='Settings'),
            ObjectList(customization_panels, heading='Custom Frontend (Advanced!)'),
        ],
    )

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
    
    @property
    def word_count(self) -> int:
        # gotten from https://stackoverflow.com/questions/42585858/display-word-count-in-blog-post-with-wagtail
        count = 0
        for block in self.content:
            if block.block_type == 'richtext' or block.block_type == 'plaintext':
                count += len(str(block.value).split())
        return count

    @property
    def minutes_to_read(self) -> int:
        """
        Assumes readers read 150 wpm on average. Returns self.world_count // 150
        """
        return self.word_count // 150

    class Meta:
        # TODO Should probably index on:
        # Author then article
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        indexes = [
            models.Index(fields=['current_section','last_modified_at']),
            models.Index(fields=['last_modified_at']),
            models.Index(fields=['category',]),
        ]


class GuideArticlePage(ArticlePage):
    pass
    # banner quote
    # banner quote source
    # subheading
    # intro text
    # series

class MagazineArticlePage(ArticlePage):
    pass

class FeatureArticlePage(ArticlePage):
    alternate_title = models.CharField(
        null=False,
        blank=True,
        default='',
        max_length=255,
    )
    optional_subtitle = models.CharField(
        null=False,
        blank=True,
        default='',
        max_length=255,
    )
    
    above_cut_lede = models.TextField(
        null=False,
        blank=True,
        default='',
    )

    # Corresponds to pseudo-field called "About" in some templates
    about_this_article = models.TextField(
        null=False,
        blank=True,
        default='',
    )

class FWTypeArticlePage(ArticlePage):
    pass