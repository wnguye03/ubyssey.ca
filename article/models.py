import datetime
from datetime import date

from dispatch.models import Article

from django import forms
from django.db import models
from django.db.models.fields import CharField
from django.forms.widgets import Select
from django.utils import timezone

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase

from videos import blocks as video_blocks

from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
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

class ArticleFeaturedImagesOrderable(Orderable):
    """
    This is based off the "ImageAttachment" class from Dispatch

    The ImageAttachment 
    """
    article_page = ParentalKey(
        "article.ArticlePage",
        related_name="featured_images",
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

    panels = [
        MultiFieldPanel(
            [
                ImageChooserPanel("image"),
                FieldPanel("caption"),
                FieldPanel("credit"),
            ],
            heading="Featured Image",
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

class ArticlePage(Page):
    #-----Main attributes-----
    template = "article/article_page.html"

    parent_page_types = [
        'specialfeaturelanding.SpecialLandingPage',
        'section.SectionPage',
    ]

    subpage_types = [] #Prevents article pages from having child pages

    tags = ClusterTaggableManager(through='article.ArticlePageTag', blank=True)

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
    published_at = models.DateTimeField(
        null=False,
        blank=False,
        default=datetime.datetime.combine(UBYSSEY_FOUNDING_DATE, datetime.time()),
        help_text = "To be explicitly shown to the reader. Articles are seperately date/timestamped for database use, so editors can explicitly override the displayed date.",
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
                FieldPanel("published_at"),
                FieldPanel("show_last_modified"),
            ],
            heading="Publication Date"
        ),
        MultiFieldPanel(
            [
                # FieldPanel("section"),
                FieldPanel("tags"),
            ],
            heading="Sections and Tags",
        ),
        MultiFieldPanel(
            [
                InlinePanel("featured_images", label="Featured Image(s)"),
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

    def save_revision_with_custom_created_at(self, user=None, submitted_for_moderation=False, approved_go_live_at=None, changed=True,
                      log_action=False, previous_revision=None, clean=True, custom_created_at_date=None):
        """
        Creates and saves a page revision. This mostly is an exact copy of the "save_revision" method of the original base Page class:
        https://github.com/wagtail/wagtail/blob/main/wagtail/core/models.py
        with the exception of the custom_created_at_date arg, which is used to 


        :param user: the user performing the action
        :param submitted_for_moderation: indicates whether the page was submitted for moderation
        :param approved_go_live_at: the date and time the revision is approved to go live
        :param changed: indicates whether there were any content changes
        :param log_action: flag for logging the action. Pass False to skip logging. Can be passed an action string.
            Defaults to 'wagtail.edit' when no 'previous_revision' param is passed, otherwise 'wagtail.revert'
        :param previous_revision: indicates a revision reversal. Should be set to the previous revision instance
        :param clean: Set this to False to skip cleaning page content before saving this revision
        :return: the newly created revision
        """
        # Raise an error if this page is an alias.
        if self.alias_of_id:
            raise RuntimeError(
                "save_revision() was called on an alias page. "
                "Revisions are not required for alias pages as they are an exact copy of another page."
            )

        if clean:
            self.full_clean()

        new_comments = self.comments.filter(pk__isnull=True)
        for comment in new_comments:
            # We need to ensure comments have an id in the revision, so positions can be identified correctly
            comment.save()

        # Create revision
        revision = self.revisions.create(
            content_json=self.to_json(),
            user=user,
            submitted_for_moderation=submitted_for_moderation,
            approved_go_live_at=approved_go_live_at,
        )

        #ONLY CUSTOM LINE IN THIS METHOD!!
        # expected value from PageRevision model:
        # created_at = models.DateTimeField(db_index=True, verbose_name=_('created at'))
        revision.created_at = custom_created_at_date

        for comment in new_comments:
            comment.revision_created = revision

        update_fields = ['comments']

        self.latest_revision_created_at = revision.created_at
        update_fields.append('latest_revision_created_at')

        self.draft_title = self.title
        update_fields.append('draft_title')

        if changed:
            self.has_unpublished_changes = True
            update_fields.append('has_unpublished_changes')

        if update_fields:
            # clean=False because the fields we're updating don't need validation
            self.save(update_fields=update_fields, clean=False)

        # Log
        logger.info("Page edited: \"%s\" id=%d revision_id=%d", self.title, self.id, revision.id)
        if log_action:
            if not previous_revision:
                PageLogEntry.objects.log_action(
                    instance=self,
                    action=log_action if isinstance(log_action, str) else 'wagtail.edit',
                    user=user,
                    revision=revision,
                    content_changed=changed,
                )
            else:
                PageLogEntry.objects.log_action(
                    instance=self,
                    action=log_action if isinstance(log_action, str) else 'wagtail.revert',
                    user=user,
                    data={
                        'revision': {
                            'id': previous_revision.id,
                            'created': previous_revision.created_at.strftime("%d %b %Y %H:%M")
                        }
                    },
                    revision=revision,
                    content_changed=changed,
                )

        if submitted_for_moderation:
            logger.info("Page submitted for moderation: \"%s\" id=%d revision_id=%d", self.title, self.id, revision.id)

        return revision

    class Meta:
        # TODO Should probably index on:
        # Subsection then article
        # Author then article
        verbose_name = "Article"
        verbose_name_plural = "Articles"
