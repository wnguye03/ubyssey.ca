from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse

from dispatch.apps.core.models import Person
from dispatch.apps.content.models import Section, Article, Author

from ubyssey.helpers import ArticleHelper

class SectionFeed(Feed):

    def __init__(self, max_items=10):
        self.max_items = max_items

    def get_object(self, request, slug):
        return Section.objects.get(name=slug)

    def title(self, section):
        return 'Ubyssey %s' % section.name

    def description(self, section):
        return 'Daily updates from Ubyssey %s' % section.name

    def link(self, section):
        return '/%s' % section.name

    def items(self, section):
        return Article.objects.filter(section=section, is_published=True).order_by('-published_at')[:self.max_items]

    def item_title(self, item):
        return item.headline

    def item_pubdate(self, item):
        return item.published_at

    def item_description(self, item):
        return item.snippet

    def item_author_name(self, item):
        auth = Author.objects.get(article_id=item.id)
        return Person.objects.get(pk=auth.person_id).full_name

    def item_link(self, item):
        return reverse('article', args=[item.section_id,item.slug])

class FrontpageFeed(Feed):

    title = 'The Ubyssey'
    link = '/'
    description = 'Daily updates from The Ubyssey'

    def __init__(self, max_items=10):
        self.max_items = max_items

    def items(self, section):
        return ArticleHelper.get_frontpage(limit = self.max_items)

    def item_title(self, item):
        return item.headline

    def item_pubdate(self, item):
        return item.published_at

    def item_description(self, item):
        return item.snippet

    def item_author_name(self, item):
        return item.get_author_string()

    def item_link(self, item):
        return reverse('article', args=[item.section_id,item.slug])
