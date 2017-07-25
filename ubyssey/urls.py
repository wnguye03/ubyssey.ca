from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from ubyssey.views.feed import FrontpageFeed, SectionFeed
from ubyssey.views.main import UbysseyTheme
from ubyssey.views.guide import GuideTheme
from ubyssey.views.magazine import MagazineTheme
from ubyssey.views.advertise import AdvertiseTheme
from ubyssey.views.events import EventsTheme

from zones import *
from widgets import *

theme = UbysseyTheme()
guide = GuideTheme()
magazine = MagazineTheme()
advertise = AdvertiseTheme()
events = EventsTheme()

theme_urls = [
    url(r'^$', theme.home, name='home'),
    url(r'^search/$', theme.search, name='search'),
    url(r'^archive/$', theme.archive, name='archive'),
    url(r'^rss/$', FrontpageFeed(), name='frontpage-feed'),

    url(r'^(?P<slug>[-\w]+)/rss/$', SectionFeed(), name='section-feed'),
    url(r'^authors/(?P<slug>[-\w]+)/$', theme.author, name='author'),
    url(r'^topic/(\d*)/$', theme.topic, name='topic'),

    # Guide to UBC
    url(r'^guide/$', guide.landing, name='guide-landing'),
    url(r'^guide/(?P<slug>[-\w]+)/$', guide.article, name='guide-article'),

    # Magazine
    url(r'^magazine/$', magazine.landing, name='magazine-landing'),
    url(r'^magazine/(?P<slug>[-\w]+)/$', magazine.article, name='magazine-article'),

    # Advertising
    url(r'^advertise/$', advertise.landing, name='advertise-landing'),

    # Elections
    url(r'^elections/$', theme.elections, name='elections'),

    url(r'^events/$', events.calendar, name='events'),
    url(r'^events/(?P<event_id>[0-9]+)/$', events.event, name='event'),

    url(r'^(?P<section>[-\w]+)/(?P<slug>[-\w]+)/$', theme.article, name='article'),
    url(r'^(?P<slug>[-\w]+)/$', theme.section, name='page'),
    url(r'^api/articles/(?P<pk>[0-9]+)/rendered/$', theme.article_ajax, name='article-ajax')
]

if settings.DEBUG:
    theme_urls += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
