from datetime import datetime

from dispatch.theme.fields import (
    CharField, TextField, ArticleField, ImageField,
    EventField, IntegerField, InvalidField, DateTimeField,
    WidgetField
)
from dispatch.theme import register
from dispatch.theme.widgets import Widget
from dispatch.apps.events.models import Event

from ubyssey.helpers import EventsHelper
from ubyssey.zones import (
    ArticleHorizontal, ArticleSidebar, FrontPage,
    HomePageSidebar, HomePageSidebarBottom
)

@register.widget
class EventWidget(Widget):
  id = 'event-widget'
  name = 'Event Widget'
  template = 'widgets/event.html'
  zones = (ArticleSidebar,)

  event = EventField('Custom Event')

  def context(self, result):
      """Select random event if custom event is not specified"""

      if not result.get('event'):
          result['event'] = EventsHelper.get_random_event()
      return result

@register.widget
class UpcomingEventsWidget(Widget):
    id = 'upcoming-events'
    name = 'Upcoming Events'
    template = 'widgets/upcoming-events.html'
    zones = (HomePageSidebar, HomePageSidebarBottom)

    featured_events = EventField('Featured Event(s)', many=True)
    featured_event_until = DateTimeField('Featured Event Time Limit')
    number_of_events = IntegerField('Number of Upcoming Events', min_value=0)

    def context(self, result):
        """Override context to add the next N events occuring to the context"""

        num_events = result['number_of_events']
        if num_events is None:
            num_events = 5

        if result['featured_event_until']:
           today = datetime.today()
           if today > result['featured_event_until'].replace(tzinfo=None):
               result['featured_events'] = None

        if result['featured_events']:
            exclusions = map(lambda e: e.pk, result['featured_events'])
        else:
            exclusions = []

        events = Event.objects \
            .filter(is_submission=False) \
            .filter(is_published=True) \
            .filter(start_time__gt=datetime.today()) \
            .exclude(pk__in=exclusions) \
            .order_by('start_time')[:num_events]

        result['upcoming'] = events

        return result

@register.widget
class UpcomingEventsHorizontalWidget(Widget):
    id = 'upcoming-events-horizontal'
    name = 'Upcoming Events Horizontal'
    template = 'widgets/upcoming-events-horizontal.html'
    zones = (ArticleHorizontal, )

    events = EventField('Override Events', many=True)

    def context(self, result):

        num = len(result['events'])

        # Target to display is 3
        if num < 3:
            events = Event.objects \
                .filter(is_submission=False) \
                .filter(is_published=True) \
                .filter(start_time__gt=datetime.today()) \
                .exclude(pk__in=map(lambda e: e.pk, result['events'])) \
                .order_by('start_time')[:3 - num]

            result['events'].extend(events)

        elif num > 3:
            result['events'] = result['events'][:3]

        return result

@register.widget
class FrontPageDefault(Widget):
    id = 'frontpage-default'
    name = 'Default Front Page'
    template = 'widgets/frontpage/default.html'
    zones = (FrontPage, )

    valid_extra_ctx_kw = ('articles', )

    # disabled until WidgetField is fixed on dispatch end
    # sidebar = WidgetField('Sidebar')
