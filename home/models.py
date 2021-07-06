from . import blocks as homeblocks

from article.models import ArticlePage
from section.models import SectionPage , CategorySnippet
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField

# Create your models here.

class HomePage(Page):
    template = "home/home_page.html"

    ajax_template = "home/ajax_section.html"
    
    parent_page_types = [
        'wagtailcore.Page',
    ]

    subpage_types = [
        'section.SectionPage',
        'authors.AllAuthorsPage',
    ]

    sections_stream = StreamField(
        [
            ("home_page_section_block", homeblocks.HomepageFeaturedSectionBlock())
        ],
        null=True,
        blank=True,
    )




    content_panels = Page.content_panels + [
        StreamFieldPanel("sections_stream", heading="Sections"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['above_cut_articles'] = self.get_above_cut_articles(max_count=6)
        context['breaking_news_article'] = self.get_breaking_articles()
        context['blog'] = self.get_section_articles(section_slug='blog')

        #if the request is ajax, it will return the requested 'section' and the feature articles under that section
        if request.is_ajax():
            section = request.GET.get('section')
            context[ 'feature_articles'] = self.get_section_articles(section_slug=section)
            context['section_name'] = section
   
        return context

    def get_above_cut_articles(self, max_count=6):
  
        return ArticlePage.objects.all().order_by('-last_published_at')[:max_count]

    above_cut_articles = property(fget=get_above_cut_articles)



    #takes a section_slug and returns the feature articles for that section
    def get_section_articles(self, section_slug):

        sectionPage = SectionPage.objects.get(slug = section_slug)
        

        return sectionPage.get_featured_articles()

    #returns the the breaking articles from each section
    def get_breaking_articles(self):

        breaking_news_artciles = []
        allsectionPages = SectionPage.objects.all()


        for section in allsectionPages:
            for article in section.get_section_articles(): 
                if article.is_breaking:
                    breaking_news_artciles.append(article)

        return breaking_news_artciles


