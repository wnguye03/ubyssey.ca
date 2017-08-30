import re, datetime

import feedparser

from django.core.management.base import BaseCommand

from ubyssey.events.models import Event, ScrapedEvent

class RSSFeed(object):

    def __init__(self, url):
        self.url = url
        self.feed = feedparser.parse(self.url)
        self.scrape_time = datetime.datetime.now()

    def create_new_events(self):
        """The new events must be added to both the Event Model and ScrapedEvent"""

        new_events = self.get_new_events()

        for event in new_events:

            # Add events to ScrapedEvent model
            GUID = event['GUID']
            scrape_time = self.scrape_time

            scraped_event = ScrapedEvent(GUID=GUID, scrape_time=scrape_time)
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
        raw_event_GUIDs = [event.get('GUID') for event in raw_events]

        for event in scraped_events:

            if event.GUID not in raw_event_GUIDs:
                event.delete()

    def get_new_events(self):
        """Returns set of new event GUIDs"""

        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        new_events = []

        # Get events in the Ubyssey database
        scraped_events = ScrapedEvent.objects.filter(scrape_time__gte=yesterday)
        previous_event_GUIDs = set(event.GUID for event in scraped_events)

        # Get events from the RSS Stream
        for event in self.get_event_data():

            if event['GUID'] not in previous_event_GUIDs:

                new_events.append(event)

        return new_events

    def get_GUID(self, url):
        """returns GUID from url"""

        guid_regex = re.search('.*(?:guid=)(.{44}).*', url)

        if guid_regex:
            return guid_regex.group(1)
        else:
            raise FeedError('Error parsing GUID from event link')

    def get_event_data(self):
        """Gets all events from feed"""
        events = []

        for event in self.feed.entries:

            guid = self.get_GUID(event.links[0]['href'])

            event_data = {
                'title': event['title'],
                'description': event['summary'],
                'GUID': guid
            }

            events.append(event_data)

        return events

class FeedError(Exception):
    pass

class Command(BaseCommand):

    def handle(self, **options):

        feedObj = RSSFeed('http://services.calendar.events.ubc.ca/cgi-bin/rssCache.pl?days=2&mode=rss')

        feedObj.create_new_events()
        feedObj.remove_old_events()
