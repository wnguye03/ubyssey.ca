import json

from django import dispatch
from article.models import ArticlePage

from dispatch.models import Article
from dispatch.modules.content import embeds

from django.core.management.base import BaseCommand, CommandError, no_translations

from section.models import SectionPage

from treebeard import exceptions as treebeard_exceptions

from wagtail.core import blocks
from wagtail.core.models import PageLogEntry
from wagtail.images.blocks import ImageChooserBlock

from videos.blocks import OneOffVideoBlock


class Command(BaseCommand):
    """
    Certain things have to be migrated to Wagtail before this can be run properly:

    Authors
    Tags
    Sections (small enough this one can be done manually)
    Subsections
    Images
    Videos
    """
    
    @no_translations
    def handle(self, *args, **options):

        # dispatch_article 
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
                        block_value = '<p>' + node['data'] + '</p>'
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
                    if len(wagtail_article_nodes) > 0 and wagtail_article_nodes[-1]['type'] == 'richtext' and block_type == 'richtext':
                        # Special case of last node being a richtext and current one also a richtext, just join them together as seperate paragraphs
                        wagtail_article_nodes[-1]['value'] = wagtail_article_nodes[-1]['value'] + block_value
                    else:
                        wagtail_streamfield_node = {
                            'type':'',
                            'value':'',
                        }
                        wagtail_streamfield_node['type'] = block_type
                        wagtail_streamfield_node['value'] = block_value
                        wagtail_article_nodes.append(wagtail_streamfield_node)

                wagtail_article.content = json.dumps(wagtail_article_nodes)

                # References for Wagtail revisions
                # Used strictly for maintaining the paper trail of articles that originally came from Dispatch
            

                wagtail_article.save_revision(log_action=True)
                if len(wagtail_article_qs) < 1:
                    log_entry_creation = PageLogEntry.objects.all()[0]
                    log_entry_creation.timestamp = dispatch_article_revision.updated_at
                    log_entry_creation.save()

                wagtail_revision = wagtail_article.get_latest_revision()
                wagtail_revision.created_at = dispatch_article_revision.updated_at
                wagtail_revision.save()
                log_entry_change = PageLogEntry.objects.all()[0]
                log_entry_change.timestamp = dispatch_article_revision.updated_at
                log_entry_change.save()

                if dispatch_article_revision.published_at:
                    wagtail_revision.publish()
                    wagtail_article.first_published_at = dispatch_article_revision.published_at
                    wagtail_article.last_published_at = dispatch_article_revision.updated_at
                    wagtail_article.save()
                    log_entry_publication = PageLogEntry.objects.all()[0]
                    log_entry_publication.timestamp = dispatch_article_revision.updated_at
                    log_entry_publication.save()