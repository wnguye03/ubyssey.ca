from django import dispatch
from article.models import ArticlePage

from dispatch.models import Article
from dispatch.modules.content import embeds

from django.core.management.base import BaseCommand, CommandError, no_translations

from section.models import SectionPage

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

        # wagtail section
        wagtail_section = SectionPage.objects.get(slug='news')
        # https://stackoverflow.com/questions/43040023/programatically-add-a-page-to-a-known-parent
        wagtail_section.add_child(instance=wagtail_article)

        for dispatch_article_revision in dispatch_article_qs:

            # Used strictly for maintaining the paper trail of articles that originally came from Dispatch
            wagtail_article.revision_id = dispatch_article_revision.revision_id
            wagtail_article.created_at_time = dispatch_article_revision.created_at
            wagtail_article.legacy_revised_at_time = dispatch_article_revision.updated_at
            wagtail_article.legacy_published_at_time = dispatch_article_revision.updated_at

            wagtail_article.slug = dispatch_article_revision.slug
            if dispatch_article_revision.seo_keyword is not None:
                wagtail_article.seo_keyword = dispatch_article_revision.seo_keyword 
            if dispatch_article_revision.seo_description is not None:
                wagtail_article.seo_description = dispatch_article_revision.seo_description
            # add something about article "template"
            # wagtail_article.
            if dispatch_article_revision.snippet is not None:
                wagtail_article.lede = dispatch_article_revision.snippet

            wagtail_article.title = dispatch_article_revision.headline

            if dispatch_article_revision.is_breaking is not None:
                wagtail_article = is_breaking
            if dispatch_article_revision.breaking_timeout is not None:
                wagtail_article.breaking_timeout =

            # Still need to do foreign keys for featured image/video and subsection!

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
                # USE JSON LIKE THIS!

                wagtail_article.content.append((block_type,block_value))
            wagtail_article.save_revision()
            if dispatch_article_revision.is_published:
                wagtail_article.publish()