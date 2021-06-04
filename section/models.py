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
class Subsection(models.Model):
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
        related_name="subsections",
    )
    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        PageChooserPanel("section_page"),
    ]
    def __str__(self):
        return "%s - %s" % (self.section_page, self.name)

class SubsectionMenuItem(wagtail_core_models.Orderable):
    subsection = ForeignKey(
        "section.Subsection",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    section = ParentalKey(
        "section.SectionPage",
        blank=True,
        null=True,
        related_name="subsection_menu",
    )
    panels = [
        SnippetChooserPanel("subsection"),
    ]
    
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
