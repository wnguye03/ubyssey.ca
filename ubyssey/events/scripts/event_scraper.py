import re, datetime

import feedparser

from ubyssey.events.models import Event, ScrapedEvent

"""http://services.calendar.events.ubc.ca/cgi-bin/rssCache.pl?days=2&mode=rss"""

class RSSFeed(object):

    def __init__(self, url):
        self.url = url
        self.feed = feedparser.parse(self.url)
        self.scrape_time = datetime.now()

    def get_new_events(self):
        """Returns set of new event GUIDs"""

        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        new_events = set()

        # Get events in the Ubyssey database
        scraped_events = ScrapedEvent.objects.filter(scrape_time__gte=yesterday)
        previous_events = set(event.GUID for event in scraped_events)

        # Get events from the RSS Stream
        for event in self.feed.entries:

            guid = self.get_GUID(event.links[0]['href'])

            if guid not in scraped_events:

                event_data = {
                    'title': event['title'],
                    'description': event['summary'],
                    'GUID': guid
                }

                new_events.add(event_data)

        return new_events

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
                is_submission=True,
                submitter_email='noreply@ubyssey.ca'
                )
            event_for_approval.save()

    def remove_old_events(self):
        """Remove events from ScrapedEvents when they are removed from the RSS feed"""

        scraped_events = ScrapedEvent.objects.all()

        new_events = self.get_new_events()
        new_event_GUIDs = [event.get('GUID') for event in new_events]

        for event in scraped_event:

            if event.GUID not in new_event_GUIDs:
                event.delete()

    def get_GUID(self, url):
        """returns GUID from url"""

        guid_regex = re.search('.*(?:guid=)(.{44}).*', url)

        if guid_regex:
            return guid_regex.group(1)
        else:
            raise FeedError('Error parsing GUID from event link')


class FeedError(Exception):
    pass


if __name__ == '__main__':
    
    feedObj = RSSFeed('http://services.calendar.events.ubc.ca/cgi-bin/rssCache.pl?days=2&mode=rss')

    feedObj.create_new_events()

    print ScrapedEvent.objects.all()
