import re
import datetime

import feedparser

from django.core.management.base import BaseCommand
from django.utils import timezone

from ubyssey.events.models import Event, ScrapedEvent

class UBCEventsRSSFeed(object):

    def __init__(self, url):
        self.url = url
        self.feed = feedparser.parse(self.url)
        self.scrape_time = timezone.now()

    def create_new_events(self):
        """The new events must be added to both the Event Model and ScrapedEvent"""

        new_events = self.get_new_events()

        for event in new_events:

            # Add events to ScrapedEvent model
            guid = event['guid']

            scraped_event = ScrapedEvent(guid=guid, scrape_time=self.scrape_time)
            scraped_event.save()

            # Add events to Event model, ready to be approved and published by staff
            event_for_approval = Event(
                title=event['title'],
                description=event['description'],
                host='CHANGE FIELD',
                start_time=self.scrape_time,
                end_time=self.scrape_time + datetime.timedelta(days=7),
                location='CHANGE FIELD',
                category='other',
                submitter_email='noreply@ubyssey.ca'
                )
            event_for_approval.save()

    def remove_old_events(self):
        """Remove events from ScrapedEvents when they are removed from the RSS feed"""

        scraped_events = ScrapedEvent.objects.all()

        raw_events = self.get_event_data()
        raw_event_guids = [event.get('guid') for event in raw_events]

        for event in scraped_events:

            if event.guid not in raw_event_guids:
                event.delete()

    def get_new_events(self):
        """Returns set of new event guids"""

        yesterday = self.scrape_time - datetime.timedelta(days=1)
        new_events = []

        # Get events in the Ubyssey database
        scraped_events = ScrapedEvent.objects.filter(scrape_time__gte=yesterday)
        previous_event_guids = set(event.guid for event in scraped_events)

        # Get events from the RSS Stream
        for event in self.get_event_data():

            if event['guid'] not in previous_event_guids:

                new_events.append(event)

        return new_events

    def get_guid(self, url):
        """returns guid from url"""

        guid_regex = re.search('.*(?:guid=)(.{44}).*', url)

        if guid_regex:
            return guid_regex.group(1)
        else:
            raise FeedError('Error parsing guid from event link')

    def get_event_data(self):
        """Gets all events from feed"""
        events = []

        for event in self.feed.entries:

            guid = self.get_guid(event.links[0]['href'])

            event_data = {
                'title': event['title'],
                'description': event['summary'],
                'guid': guid
            }

            events.append(event_data)

        return events

class FeedError(Exception):
    pass

class Command(BaseCommand):

    def handle(self, **options):

        feedObj = UBCEventsRSSFeed('http://services.calendar.events.ubc.ca/cgi-bin/rssCache.pl?days=2&mode=rss')

        feedObj.create_new_events()
        feedObj.remove_old_events()
