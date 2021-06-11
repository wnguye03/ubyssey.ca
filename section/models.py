from django.db.models.fields import CharField
from article.models import ArticlePage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.shortcuts import render

from django_extensions.db.fields import AutoSlugField

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.core import models as wagtail_core_models
from wagtail.contrib.routable_page.models import route, RoutablePageMixin
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet


#-----Snippet models-----
@register_snippet
class CategorySnippet(models.Model):
    """
    Formerly known as a 'Subsection'
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
        related_name="categories",
    )
    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        PageChooserPanel("section_page"),
    ]
    def __str__(self):
        return "%s - %s" % (self.section_page, self.name)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

#-----Orderable models-----
class CategoryMenuItem(wagtail_core_models.Orderable):
    category = ForeignKey(
        "section.CategorySnippet",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    section = ParentalKey(
        "section.SectionPage",
        blank=True,
        null=True,
        related_name="category_menu",
    )
    panels = [
        SnippetChooserPanel("category"),
    ]
    
#-----Page models-----
class SectionablePage(wagtail_core_models.Page):
    """
    Pages in the site heirarchy tend to belong to a section.
    Sections correspond to child nodes of the HomePage that themselves have many children.
    Therefore all SectionablePages have built-in capacity to traverse backwards up the Page tree
    """
    is_creatable = False #no page should ever JUST be a sectionable page. This is an "abstract" page
    current_section = CharField(
        max_length=255, #should contain the SLUG of the current section, not its name. Max length reflects max Wagtail slug length
        null=False,
        blank=True,
        default='',
    ) 

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["current_section"] = self.current_section
        return context

    def save(self, *args, **kwargs):
        """
        Ensures the page's current section is synced with its parents/ancestors
        Or else, if this is a section page, its section is itself
        """
        ancestors_qs = self.get_ancestors()
        if len(ancestors_qs) <= 1:
            # if there is at most one ancestor, this must be a section page, so use its slug for current section
            self.current_section = self.slug
        else:
            # otherwise, we have some non-section page that should be able to learn what section it's in from its parent
            try:
                self.current_section = ancestors_qs.last().current_section
            except Exception as e:
                self.current_section = 'ERROR_SECTION'

        return super().save(*args, **kwargs)

    class Meta:
        abstract = True

class SectionPage(SectionablePage):
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
                InlinePanel("category_menu"),
            ],
            heading="Category Menu",
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

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"
