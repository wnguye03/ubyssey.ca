from dispatch.theme import register
from dispatch.theme.widgets import Widget
from dispatch.theme.fields import CharField, EventField
from zones import EventSidebar

@register.widget
class EventWidget(Widget):
  id = 'custom'
  name = 'Event Widget'
  template = 'widgets/event.html'
  zones = (EventSidebar,)

  title = CharField('title')

  event = EventField('event')
