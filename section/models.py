from django.db.models.fields import CharField
from article.models import ArticlePage
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.shortcuts import render

from django_extensions.db.fields import AutoSlugField

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.core import models as wagtail_core_models
from wagtail.contrib.routable_page.models import route, RoutablePageMixin
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from taggit.models import TagBase, ItemBase


#-----Orderable models-----
@register_snippet
class Subsection(wagtail_core_models.Orderable):
    """
    This closely corresponds to the Dispatch model that is (mis-)named "Author"
    """
    name = CharField(
        blank=False,
        null=False,
        max_length=100
    )
    slug = AutoSlugField(
        populate_from="name",
        editable=True,
        blank=False,
        null=False,
        max_length=100
    )
    section_page = ParentalKey(
        "section.SectionPage",
        related_name="subsection_menu",
    )
    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]
    def __str__(self):
        return "%s - %s" % (self.section_page, self.name)

# class PrefilteredSubsectionManager(models.Manager):
#     def __init__(self, slug=''):
#         self.section_page_slug = slug

#     def get_queryset(self):
#         qs = super().get_queryset()
#         if self.section_page_slug != '': 
#             qs.filter(section_page__slug=self.section_page_slug)
#         return qs

@register_snippet
class PrefilteredSubsection(Subsection):
    """
    Proxy Class for Subsection
    This is a bit of a strange pattern. It was taken from the below StackOverflow
    https://stackoverflow.com/questions/56915888/how-can-i-customise-the-queryset-in-snippetchooserpanel-within-wagtail
    """
    def __init__(self):
        super().__init__()
        self.section_page_slug = ''

    # objects = PrefilteredSubsectionManager()

    class Meta:
        proxy = True

#-----Page models-----

class SectionPage(wagtail_core_models.Page):
    template = 'section/section_page.html'

    subpage_types = [
        'article.ArticlePage',
        'specialfeaturelanding.SpecialLandingPage',
    ]
    parent_page_types = [
        'home.HomePage',
    ]

    content_panels = wagtail_core_models.Page.content_panels + [
        MultiFieldPanel(
            [
                InlinePanel("subsection_menu"),
            ],
            heading="Subsection(s)",
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        all_articles = ArticlePage.objects.live().public().descendant_of(self)
        if 'subsection_slug' in kwargs:
            pass
            # TODO filter ArticlePage by subsection once that field is implemented properly
            #all_articles.filter

        all_articles.order_by('-first_published_at')
        # Paginate all posts by 15 per page
        paginator = Paginator(all_articles, per_page=15)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            articles = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            articles = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            articles = paginator.page(paginator.num_pages)

        context["articles"] = articles
        return context
        
    @route(r'^subsection/(?P<subsection_slug>[-\w]+)/$', name='subsection_view')
    def subsection_view(self, request, subsection_slug):
        context = self.get_context(request, subsection_slug=subsection_slug)
        return render(request, 'section/section_page.html', context)
