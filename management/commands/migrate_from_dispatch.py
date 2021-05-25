from article.models import ArticlePage

from dispatch.models import Article

from django.core.management.base import BaseCommand, CommandError, no_translations

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class Command(BaseCommand):
    
    @no_translations
    def handle(self, *args, **options):

        # dispatch_article 
        dispatch_article_qs = Article.objects.filter(slug='keegan-test').order_by('revision_id')
        
        # wagtail_article
        wagtail_article = ArticlePage()
        for dispatch_article_revision in dispatch_article_qs(''):
            for node in dispatch_article_revision.content:
                pass
                # figure out what the type of the embed is (embed_type). set the appropriate block_type
                
                #wagtail_article.content