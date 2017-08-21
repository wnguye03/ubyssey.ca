import calendar
from pytz import timezone
from collections import OrderedDict
from datetime import date

from django.http import Http404
from django.shortcuts import render
from django.conf import settings
from django.core.urlresolvers import reverse
from dispatch.apps.events.models import Event
from dispatch.apps.frontend.themes.default import DefaultTheme

from ubyssey.helpers import EventsHelper

class EventsTheme(DefaultTheme):
    def calendar(self, request):
        category = request.GET.get('category')
        months = request.GET.get('months')
        start = request.GET.get('start')
        end = request.GET.get('end')

        events = EventsHelper.get_calendar_events(category=category, months=months, start=start, end=end)
        events_by_date = EventsHelper.group_events_by_date(events)

        context = {
            'meta': {
                'title': 'Calendar',
                'description': 'Ubyssey calendar of events',
                'url': "%s%s" % (settings.BASE_URL, reverse('events'))
            },
            'events_by_date': events_by_date,
            'this_year': date.today().year,
            'category': category
        }

        return render(request, 'events/calendar.html', context)

    def get_event_meta(self, event):
        meta_image = None
        if event.image:
            meta_image = event.image.url

        return {
            'title': event.title,
            'description': event.description,
            'image': "%s%s" %(settings.BASE_URL, meta_image),
            'url': "%sevent/%s/" % (settings.BASE_URL, event.id)
        }

    def event(self, request, event_id):
        try:
            event = EventsHelper.get_event(event_id)
        except:
            raise Http404('Event could not be found.')

        upcoming = Event.objects \
            .filter(is_submission=False) \
            .filter(is_published=True) \
            .filter(start_time__gt=date.today()) \
            .order_by('start_time')[:3]

        context = {
            'meta': self.get_event_meta(event),
            'event': event,
            'upcoming': upcoming
        }

        return render(request, 'events/event.html', context)
