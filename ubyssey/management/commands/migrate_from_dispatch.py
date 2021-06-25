import json
import hashlib
import requests

from article.models import ArticlePage, ArticleAuthorsOrderable
from authors.models import AuthorPage, AllAuthorsPage

from dispatch import models as dispatch_models
from dispatch.modules.content import embeds

from django import dispatch
from django.conf import settings
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand, CommandError, no_translations

from io import BytesIO
from images.models import UbysseyImage as CustomImage

from section.models import SectionPage

from treebeard import exceptions as treebeard_exceptions

from wagtail.core import blocks
from wagtail.core.models import PageLogEntry
from wagtail.images.models import Image
from wagtail.images.blocks import ImageChooserBlock

from videos.blocks import OneOffVideoBlock


def _migrate_all_images():
    # Documentation this was originally taken from: http://devans.mycanadapayday.com/programmatically-adding-images-to-wagtail/

    old_images = dispatch_models.Image.objects.all()
    wagtail_images = CustomImage.objects.all()
    for old_image in old_images:
        has_been_sent_to_wagtail = any(str(old_image.img) == wagtail_image.legacy_filename for wagtail_image in wagtail_images)
        if not has_been_sent_to_wagtail:
            url = old_image.get_absolute_url()
            if settings.DEBUG:
                url = 'http://localhost:8000' + url
            http_res = requests.get(url)

            if http_res.status_code == 200:    
                wagtail_image_title = 'default_title' #should never actually be used, but just in case
                if not old_image.title:
                    wagtail_image_title = str(old_image.img)
                else:
                    wagtail_image_title = old_image.title
                image_file = ImageFile(BytesIO(http_res.content), name=wagtail_image_title)
                wagtail_image = CustomImage(title=wagtail_image_title, file=image_file)

                wagtail_image.legacy_filename = str(old_image.img)
                wagtail_image.created_at = old_image.created_at
                wagtail_image.updated_at = old_image.updated_at
                wagtail_image.save()

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
        
        # dispatch persons
        # FIRST we go without taking images into account. Likewise for Images. Then we'll go back 
        all_authors_page = AllAuthorsPage.objects.get(slug='authors')
        dispatch_persons_qs = dispatch_models.Person.objects.all()
        for person in dispatch_persons_qs:
            wagtail_authors_qs = AuthorPage.objects.filter(slug=person.slug)
            if len(wagtail_authors_qs) > 0:
                continue # go to next person if this person has already been created
            wagtail_author = AuthorPage()
            wagtail_author.slug = person.slug
            wagtail_author.full_name = person.full_name
            wagtail_author.title = person.full_name
            if person.title:
                wagtail_author.ubyssey_role = person.title
            if person.facebook_url:
                wagtail_author.facebook_url = person.facebook_url
            if person.twitter_url:
                wagtail_author.twitter_url = person.twitter_url
            try:
                all_authors_page.add_child(instance=wagtail_author)
            except treebeard_exceptions.NodeAlreadySaved as e:
                print(e)
            wagtail_author.save_revision(log_action=False).publish()
            print(AuthorPage.objects.filter(slug=person.slug))

        # dispatch_article 
        dispatch_head_articles_qs = dispatch_models.Article.objects.filter(head=True).order_by('-published_at')        

        for head_article in dispatch_head_articles_qs:
            current_slug = head_article.slug
            
            dispatch_article_qs = dispatch_models.Article.objects.filter(slug=current_slug).order_by('revision_id')        
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
                    # WARNING: what does this do? db hit and then...?
                    wagtail_article_qs.get(slug=current_slug)

                # Headline/Title
                wagtail_article.title = dispatch_article_revision.headline

                # Section
                try:
                    wagtail_section.add_child(instance=wagtail_article)
                except treebeard_exceptions.NodeAlreadySaved as e:
                    print(e)
                # Author
                for dispatch_author in dispatch_article_revision.authors.all():
                    # First we make sure there's any author page corresponding to this author
                    if AuthorPage.objects.get(slug=dispatch_author.person.slug):
                        # Unfortunately, first we need to see if there is already an author orderable corresponding to this author already
                        # Otherwise we'll just get a bunch of redundant orderables
                        has_author_already = any(article_author.author.slug == dispatch_author.person.slug for article_author in wagtail_article.article_authors.all())
                        if not has_author_already:
                            wagtail_author_orderable = ArticleAuthorsOrderable()
                            wagtail_author_orderable.article_page = wagtail_article
                            wagtail_author_orderable.author_role = dispatch_author.type
                            wagtail_author_orderable.sort_order = dispatch_author.order
                            wagtail_author_orderable.author = AuthorPage.objects.get(slug=dispatch_author.person.slug)
                            wagtail_author_orderable.save()

                # SEO stuff
                if dispatch_article_revision.seo_keyword is not None:
                    wagtail_article.seo_keyword = dispatch_article_revision.seo_keyword 
                if dispatch_article_revision.seo_description is not None:
                    wagtail_article.seo_description = dispatch_article_revision.seo_description
                # add something about article "template"
                
                # Lede
                if dispatch_article_revision.snippet is not None:
                    wagtail_article.lede = dispatch_article_revision.snippet
                # Breaking
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

                    # Turns out keeping blocks on a paragraph-by-paragraph basis makes keeping track of present revisions make more sense, so we do not use the below if statement
                    # it may be useful for something though, so it lives on in comments
                    # if len(wagtail_article_nodes) > 0 and wagtail_article_nodes[-1]['type'] == 'richtext' and block_type == 'richtext':
                    #    # Special case of last node being a richtext and current one also a richtext, just join them together as seperate paragraphs
                    #    wagtail_article_nodes[-1]['value'] = wagtail_article_nodes[-1]['value'] + block_value
                    # else:

                    wagtail_streamfield_node = {
                        'type':'',
                        'value':'',
                    }
                    wagtail_streamfield_node['type'] = block_type
                    wagtail_streamfield_node['value'] = block_value
                    wagtail_streamfield_node['id'] = hashlib.sha1(str(wagtail_streamfield_node).encode('utf-8')).hexdigest()
                    wagtail_article_nodes.append(wagtail_streamfield_node)

                wagtail_article.content = json.dumps(wagtail_article_nodes)

                # Wagtail revision created corresponding to the Dispatch revision
                wagtail_article.save_revision(log_action=True)
                
                # Ensure all Wagtail _creation_ timestamps correspond to their Dispatch counterparts
                if len(wagtail_article_qs) < 1:
                    log_entry_creation = PageLogEntry.objects.all()[0]
                    log_entry_creation.timestamp = dispatch_article_revision.updated_at
                    log_entry_creation.save()
                # Ensure all Wagtail _draft_ timestamps correspond to their Dispatch counterparts
                wagtail_revision = wagtail_article.get_latest_revision()
                wagtail_revision.created_at = dispatch_article_revision.updated_at
                wagtail_revision.save()
                log_entry_change = PageLogEntry.objects.all()[0]
                log_entry_change.timestamp = dispatch_article_revision.updated_at
                log_entry_change.save()
                wagtail_article.latest_revision_created_at = dispatch_article_revision.updated_at
                wagtail_article.save()
                # Ensure all Wagtail _publish_ timestamps correspond to their Dispatch counterparts
                if dispatch_article_revision.published_at:
                    wagtail_revision.publish()
                    wagtail_article.first_published_at = dispatch_article_revision.published_at
                    wagtail_article.last_published_at = dispatch_article_revision.updated_at
                    wagtail_article.save()
                    log_entry_publication = PageLogEntry.objects.all()[0]
                    log_entry_publication.timestamp = dispatch_article_revision.updated_at
                    log_entry_publication.save()