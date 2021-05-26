from article.models import ArticlePage

from dispatch.models import Article
from dispatch.modules.content import embeds

from django.core.management.base import BaseCommand, CommandError, no_translations

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from videos.blocks import OneOffVideoBlock


class Command(BaseCommand):
    
    @no_translations
    def handle(self, *args, **options):

        # dispatch_article 
        dispatch_article_qs = Article.objects.filter(slug='keegan-test').order_by('revision_id')
        
        # wagtail_article
        wagtail_article = ArticlePage()
        for dispatch_article_revision in dispatch_article_qs:
            for node in dispatch_article_revision.content:
                # figure out what the type of the embed is (node_type). set the appropriate block_type
                node_type = node['type']
                block_type = 'richtext'
                if node_type == 'paragraph':
                    block_type = 'richtext'
                    block_value = node['data']
                elif node_type == 'dropcap':
                    block_type = 'dropcap'
                    block_value = node['data']['paragraph']
                elif node_type == 'pagebreak':
                    block_type = 'raw_html'
                    block_value = '<div class="page-break"><hr class = "page-break"></div>'
                elif node_type == 'widget':
                    # This is the "worst case scenario" way of migrating old Dispatch stuff, when it depdnds on features we no longer intend to support
                    block_type = 'raw_html'
                    block_value = embeds.WidgetEmbed.render(data=node.data)
                # elif node_type == 'video':
                #     block_type = 'video'
                #     block_value = blocks.StructValue()
                #     block_value['video_embed'] 

                # NOTE: https://stackoverflow.com/questions/34200844/how-can-i-programmatically-add-content-to-a-wagtail-streamfield
                # USE JSON LIKE THIS!

                wagtail_article.content.append((block_type,block_value))

                print(wagtail_article.content)