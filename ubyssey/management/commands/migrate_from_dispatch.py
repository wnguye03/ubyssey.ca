import json

from django import dispatch
from article.models import ArticlePage

from dispatch.models import Article
from dispatch.modules.content import embeds

from django.core.management.base import BaseCommand, CommandError, no_translations

from section.models import SectionPage

from treebeard import exceptions as treebeard_exceptions

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from videos.blocks import OneOffVideoBlock


class Command(BaseCommand):
    
    @no_translations
    def handle(self, *args, **options):

        # dispatch_article 
        current_slug = 'keegan-test'
        dispatch_head_articles_qs = Article.objects.filter(head=True).order_by('-published_at')        

        for head_article in dispatch_head_articles_qs:
            current_slug = head_article.slug
            
            dispatch_article_qs = Article.objects.filter(slug=current_slug).order_by('revision_id')        
            # wagtail_article
            wagtail_article = ArticlePage()
            # wagtail section
            wagtail_section = SectionPage.objects.get(slug='news')
            # https://stackoverflow.com/questions/43040023/programatically-add-a-page-to-a-known-parent

            for dispatch_article_revision in dispatch_article_qs:

                # first check if there's an article with this slug already:

                wagtail_article_qs = ArticlePage.objects.filter(slug=current_slug)

                if len(wagtail_article_qs) < 1:
                    #initialize a new wagtail article
                    wagtail_article = ArticlePage()
                    wagtail_article.created_at_time = dispatch_article_revision.created_at
                    wagtail_article.slug = dispatch_article_revision.slug
                else:
                    wagtail_article_qs.get(slug=current_slug)

                # Used strictly for maintaining the paper trail of articles that originally came from Dispatch
                wagtail_article.revision_id = dispatch_article_revision.revision_id
                wagtail_article.legacy_revised_at_time = dispatch_article_revision.updated_at
                if dispatch_article_revision.published_at is not None:
                    wagtail_article.legacy_published_at_time = dispatch_article_revision.published_at

                wagtail_article.title = dispatch_article_revision.headline

                try:
                    wagtail_section.add_child(instance=wagtail_article)
                except treebeard_exceptions.NodeAlreadySaved as e:
                    print(e)

                if dispatch_article_revision.seo_keyword is not None:
                    wagtail_article.seo_keyword = dispatch_article_revision.seo_keyword 
                if dispatch_article_revision.seo_description is not None:
                    wagtail_article.seo_description = dispatch_article_revision.seo_description
                # add something about article "template"
                # wagtail_article.
                if dispatch_article_revision.snippet is not None:
                    wagtail_article.lede = dispatch_article_revision.snippet

                if dispatch_article_revision.is_breaking is not None:
                    wagtail_article.isbreaking = bool(dispatch_article_revision.is_breaking)
                if dispatch_article_revision.breaking_timeout is not None:
                    wagtail_article.breaking_timeout = dispatch_article_revision.breaking_timeout

                # Still need to do foreign keys for featured image/video and subsection!

                wagtail_article_nodes = []

                for node in dispatch_article_revision.content:
                    # copy data from dispatch_article_revision.content to wagtail.article
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
                    # https://stackoverflow.com/questions/47788080/how-can-i-create-page-and-set-its-streamfield-value-programmatically
                    # USE JSON LIKE THIS!
                    wagtail_streamfield_node = {
                        'type':'',
                        'value':'',
                    }
                    wagtail_streamfield_node['type'] = block_type
                    wagtail_streamfield_node['value'] = block_value
                    wagtail_article_nodes.append(wagtail_streamfield_node)
                
                wagtail_article.content = json.dumps(wagtail_article_nodes)
                if dispatch_article_revision.is_published:
                    wagtail_article.save_revision().publish()
                else:
                    wagtail_article.save_revision()
