from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.conf import settings
from dispatch.apps.frontend.themes.default import DefaultTheme

from ubyssey.events.facebook import FacebookEvent, FacebookEventError
from ubyssey.events.forms import EventForm
from ubyssey.events.models import Event
from ubyssey.helpers import EventsHelper

import calendar
from pytz import timezone
from collections import OrderedDict
from datetime import date

def submit_landing(request):
    return render(request, 'events/submit/landing.html')

def submit_success(request):
    return render(request, 'events/submit/success.html')

def submit_form(request):
    facebook_url = request.POST.get('facebook_url')
    facebook_error = False

    if request.POST.get('facebook_import') and facebook_url is not None:
        try:
            event = FacebookEvent(facebook_url)
            data = event.get_data()
            form = EventForm(initial=data)
        except FacebookEventError:
            facebook_error = True
            form = EventForm()

    elif request.method == 'POST':
        form = EventForm(request.POST, request.FILES)

        if form.is_valid():
            form.is_submission = True
            form.save()

            return redirect(submit_success)
    else:
        form = EventForm()

    return render(request, 'events/submit/form.html', {'form': form, 'facebook_error': facebook_error})

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

    context = {
        'meta': self.get_event_meta(event),
        'event': event
    }

    return render(request, 'events/event.html', context)
