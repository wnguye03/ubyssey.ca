from datetime import date

from dispatch.theme import register
from dispatch.theme.widgets import Widget
from dispatch.theme.fields import CharField, EventField
from dispatch.apps.events.models import Event

from zones import EventSidebar, HomePageSidebar

@register.widget
class EventWidget(Widget):
  id = 'custom'
  name = 'Event Widget'
  template = 'widgets/event.html'
  zones = (EventSidebar,)

  title = CharField('Title')

  event = EventField('Event')

@register.widget
class UpcomingEvents(Widget):
  id = 'upcoming-events'
  name = 'Upcoming Events'
  template = 'widgets/upcoming-events.html'
  zones = (HomePageSidebar,)

  featured_events = EventField('Featured Events', many=True)
  number_of_events = CharField('Number of Events')

  def prepare_data(self):
    result = super(UpcomingEvents, self).prepare_data()
    today = date.today()

    N = int(result['number_of_events'], base=10)

    featured_ids = []
    if isinstance(result['featured_events'], list):
        for e in result['featured_events']:
            featured_ids.append(e.pk)

    events = Event.objects \
        .filter(is_submission=False) \
        .filter(is_published=True) \
        .filter(start_time__gt=today) \
        .exclude(pk__in=featured_ids) \
        .order_by('start_time')[:N]

    result['upcoming'] = events

    return result
