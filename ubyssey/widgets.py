from datetime import datetime

from dispatch.theme.fields import (
    CharField, TextField, ArticleField, ImageField,
    EventField, IntegerField, InvalidField, DateTimeField
)
from dispatch.theme import register
from dispatch.theme.widgets import Widget
from dispatch.apps.events.models import Event

from ubyssey.helpers import EventsHelper
from ubyssey.zones import ArticleSidebar, HomePageSidebar, HomePageSidebarBottom

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

    featured_event = EventField('Featured Event', many=False)
    featured_event_until = DateTimeField('Featured Event Time Limit')
    number_of_events = IntegerField('Number of Events', min_value=0)

    def context(self, result):
        """Override context to add the next N events occuring to the context"""

        num_events = result['number_of_events']
        if num_events is None:
            num_events = 5

        if result['featured_event_until']:
            today = datetime.today()
            if today > result['featured_event_until'].replace(tzinfo=None):
                result['featured_event'] = None

        # exclude the featured event from showing up in the other list
        if result['featured_event']:
            featured_id = result['featured_event'].pk
        else:
            featured_id = None

        events = Event.objects \
            .filter(is_submission=False) \
            .filter(is_published=True) \
            .filter(start_time__gt=datetime.today()) \
            .exclude(pk=featured_id) \
            .order_by('start_time')[:num_events]

        result['upcoming'] = events

        return result
