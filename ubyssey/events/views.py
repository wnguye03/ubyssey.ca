import re
from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, Http404
from django.conf import settings

from ubyssey.events.sources import FacebookEvent, UBCEvent, NoEventHandler, EventError
from ubyssey.events.forms import EventForm
from ubyssey.events.models import Event

def submit_landing(request):
    return render(request, 'events/submit/landing.html')

def submit_success(request):
    return render(request, 'events/submit/success.html')

def submit_form(request):
    event_url = request.POST.get('event_url')
    url_error = False

    if request.POST.get('url_import') and event_url is not None:

        sources = {
            'calendar.events.ubc.ca': UBCEvent,
            'facebook.com': FacebookEvent
        }

        hostname = get_host_from_url(event_url)

        if hostname in sources:
            handler = sources[hostname]
        else:
            handler = NoEventHandler

        try:
            event = handler(event_url)
            data = event.get_data()
            data['event_type'] = event.event_type
            form = EventForm(initial=data)
        except EventError:
            url_error = True
            form = EventForm()

    elif request.method == 'POST':
        form = EventForm(request.POST, request.FILES)

        if form.is_valid():

            event = form.save(commit=False)
            event.is_submission = True
            event.save()
            return redirect(submit_success)
    else:
        form = EventForm()

    return render(request, 'events/submit/form.html', {'form': form, 'url_error': url_error})

def event(request, event_id):
    try:
        event = Event.objects.get_published(event_id)
    except Event.DoesNotExist:
        raise Http404('Event could not be found.')

    upcoming = Event.objects \
        .filter(is_submission=False) \
        .filter(is_published=True) \
        .filter(start_time__gt=date.today()) \
        .order_by('start_time')[:3]

    context = {
        'meta': get_event_meta(event),
        'event': event,
        'upcoming': upcoming,
        'info_text': 'Hosting an event? Promote it for free on our website!',
        'info_link_text': 'Submit your event',
        'info_link': reverse('events-submit-landing')
    }

    return render(request, 'events/event.html', context)

def calendar(request):
    category = request.GET.get('category')
    months = request.GET.get('months')
    start = request.GET.get('start')
    end = request.GET.get('end')

    events = Event.objects.get_calendar_events(category=category, months=months, start=start, end=end)
    events_by_date = Event.objects.group_events_by_date(events)

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

def get_event_meta(event):
    meta_image = None
    if event.image:
        meta_image = event.image.url

    return {
        'title': event.title,
        'description': event.description,
        'image': "%s%s" %(settings.BASE_URL, meta_image),
        'url': "%sevent/%s/" % (settings.BASE_URL, event.id)
    }

def get_host_from_url(url):
    """Parses URL against regex to pull out the hostname"""

    # Match numbers that is the event id from the url and return them
    m = re.search('.*(facebook\.com|calendar\.events\.ubc\.ca)+.*', url)

    if m:
        return m.group(1)
    else:
        raise EventError('URL provided is not a valid Facebook event or UBC event url')
