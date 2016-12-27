from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse

from dispatch.apps.content.models import Article

from ubyssey.helpers import ArticleHelper

class FrontpageFeed(Feed):
    title = 'Ubyssey Front Page'
    link = '/'
    description = 'Updates from the Ubyssey'

    def __init__(self, max_items=10):
        self.max_items = max_items
        
    def items(self):
        return ArticleHelper.get_frontpage()[:self.max_items]

    def item_title(self, item):
        return item.headline

    def item_description(self, item):
        return item.snippet

    def item_link(self, item):
        return reverse('article', args=[item.section_id,item.slug])
