from datetime import date

from dispatch.theme import register
from dispatch.theme.widgets import Widget
from dispatch.theme.fields import CharField, EventField
from dispatch.apps.events.models import Event

from zones import HomePageSidebar, HomePageSidebarBottom

@register.widget
class UpcomingEvents(Widget):
  id = 'upcoming-events'
  name = 'Upcoming Events'
  template = 'widgets/upcoming-events.html'
  zones = (HomePageSidebar, HomePageSidebarBottom)

  featured_event = EventField('Featured Events', many=False)
  number_of_events = CharField('Number of Events')

  def prepare_data(self):
    """Overide prepare_data to add the next N events occuring to the context"""

    result = super(UpcomingEvents, self).prepare_data()

    try:
        N = int(result['number_of_events'], base=10)
    except:
        N = 5

    # exclude the featured event from showing up in the other list
    if result['featured_event']:
        featured_id = result['featured_event'].pk
    else:
        featured_id = None

    events = Event.objects \
        .filter(is_submission=False) \
        .filter(is_published=True) \
        .filter(start_time__gt=date.today()) \
        .exclude(pk=featured_id) \
        .order_by('start_time')[:N]

    result['upcoming'] = events

    return result
