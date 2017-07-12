from dispatch.theme.fields import CharField, TextField, ArticleField, ImageField, EventField, InvalidField
from dispatch.theme import register
from dispatch.theme.widgets import Zone, Widget
from dispatch.apps.events.models import Event

class Sidebar(Zone):

    id = 'sidebar'
    name = 'Sidebar'

class SingleEventWidget(Widget):

    id = 'single-event'
    name = 'Single Event'

    template = 'templates/single_event_widget.html'

    zones = [Sidebar]

    title = CharField('Featured Event')

    def context(self, data):

        event = Event.objcts.filter(is_published=True).order_by('start_time')[:1]

        print event.start_time

        data['events'].append({
            'title': event.title,
            'start_day': event.start_time.day,
            'start_month': event.start_time.month,
            'start_time': event.start_time,
            'end_time': event.end_time,
            'image': event.image,
            'location': event.loction
        })
