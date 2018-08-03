import kronos
import json
import requests

from pywebpush import webpush, WebPushException

from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse
from dispatch.models import Article, Notification, Subscription

# Setup cron jobs

# Cron task for pushing notifications, if there are any, every minute
@kronos.register('* * * * *')
def send_notifications():
    url = "%s%s" % (settings.BASE_URL.strip('/'), reverse('api-notifications-push'))
    requests.post(url)

# Cron task for counting subscribers daily at midnight
@kronos.register('0 0 * * *')
def count_subscribers():
    url = "%s%s" % (settings.BASE_URL.strip('/'), reverse('api-subscriptioncount-list'))
    requests.post(url)
