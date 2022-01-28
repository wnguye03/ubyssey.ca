from django.db import models
from django.utils import timezone
from section.sectionable.models import SectionablePage # self made abstract model

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from django_extensions.db.fields import AutoSlugField

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from taggit.models import TaggedItemBase
from taggit.managers import TaggableManager

from ubyssey.validators import validate_youtube_url

from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.core.models import Orderable, Page
from wagtail.snippets.models import register_snippet

#-----Taggit stuff-----

class VideoTag(TaggedItemBase):
    content_object = ParentalKey('videos.VideoSnippet', on_delete=models.CASCADE, related_name='tagged_items')

#-----Orderable models-----

class VideoAuthorsOrderable(Orderable):
    """
    This closely corresponds to the Dispatch model that is (mis-)named "Author"
    """
    video = ParentalKey(
        "videos.VideoSnippet",
        related_name="video_authors",
    )
    author = models.ForeignKey(
        'authors.AuthorPage',
        on_delete=models.CASCADE,
    )
    panels = [
        MultiFieldPanel(
            [
                PageChooserPanel("author"),
            ],
            heading="Author",
        ),
    ]

# def videos(context):
#     return {
#         'videos': VideoSnippet.objects.all(),
#         'request': context['request'],
#     }

class VideosPage(SectionablePage):
    template = 'videos/videos_page.html'

    parent_page_types = [
        'home.HomePage',
    ]
    max_count_per_parent = 1
    show_in_menus_default = True
    
    def __str__(self):
        """String rep of VideosPage"""
        return self.title

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        all_videos = VideoSnippet.objects.all()

        paginator = Paginator(all_videos, per_page=15)

        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            paginated_videos = paginator.page(page)
            
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            paginated_videos = paginator.page(1)
        
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            paginated_videos = paginator.page(paginator.num_pages)

        context["videos"] = VideoSnippet.objects.all()
        
        return context


#-----Snippet models-----

@register_snippet
class VideoSnippet(ClusterableModel):

    title = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )
    slug = AutoSlugField(
        populate_from="title",
        editable=True,
        max_length=255,
        primary_key=True,
        unique=True,
        db_index=True,
        null=False,
        blank=False,
        default='',
    )
    url = models.URLField(
        max_length=500,
        null=False,
        blank=False,
        default='',
        validators=[validate_youtube_url,]
    )

    # authors = models.ManyToManyField(related_name='video_authors')
    tags = TaggableManager(through=VideoTag, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"), 
                FieldPanel("slug"),
                FieldPanel("url"),
            ],
            heading="Necessary Fields"
        ),
        MultiFieldPanel(
            [
                InlinePanel("video_authors", max_num=20, label="Author"),
            ],
            heading="Author(s)"
        ),
        MultiFieldPanel(
            [
                FieldPanel("tags"), 
            ],
            heading="Tags"
        ),
    ]
    
    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"