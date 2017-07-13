from datetime import datetime

from dispatch.theme.fields import CharField, TextField, ArticleField, ImageField, EventField, InvalidField
from dispatch.theme import register
from dispatch.theme.widgets import Zone, Widget
from dispatch.apps.events.models import Event
from zones import EventSidebar


@register.widget
class SingleEventWidget(Widget):

    id = 'single-event'
    name = 'Single Event'

    template = 'widgets/single_event_widget.html'

    zones = [EventSidebar]

    title = CharField('Event Title')

    def context(self, data):

        event = Event.objects.filter(is_published=True).order_by('start_time')[:1][0]

        data['events'] = {
            'title': event.title,
            'start_day': event.start_time.day,
            'start_month': event.start_time.strftime('%b'),
            'start_time': event.start_time,
            'end_time': event.end_time,
            'image': event.image.url,
            'location': event.location
        }

        return data

@register.widget
class EventWidget(Widget):
  id = 'custom'
  name = 'Event Widget'
  template = 'widgets/event.html'
  zones = (EventSidebar,)

  title = CharField('title')

  event = EventField('event')
