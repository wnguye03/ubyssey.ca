from datetime import datetime

from dispatch.theme.fields import CharField, TextField, ArticleField, ImageField, EventField, InvalidField
from dispatch.theme import register
from dispatch.theme.widgets import Zone, Widget
from dispatch.apps.events.models import Event

from ubyssey.zones import EventSidebar

@register.widget
class EventWidget(Widget):
  id = 'custom'
  name = 'Event Widget'
  template = 'widgets/event.html'
  zones = (EventSidebar,)

  title = CharField('title')

  event = EventField('event')
