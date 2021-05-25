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
                # figure out what the type of the embed is (node_type). set the appropriate block_type
                node_type = node['type']
                block_type = 'richtext'
                if node_type == 'paragraph':
                    block_type = 'richtext'
                    block_value = node['value']
                                
                wagtail_article.content.append((block_type,block_value))

                print(wagtail_article.content.append)