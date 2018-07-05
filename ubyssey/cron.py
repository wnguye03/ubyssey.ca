import kronos
import json

from pywebpush import webpush, WebPushException
from dispatch.models import Notification, Subscription

# Cron job helper functions

def push_notifications(article):
    # grab each endpoint from list in database and make a push
    data={
        'headline': article.headline,
        'url': article.get_absolute_url(),
        'snippet': article.snippet,
        'image': article.featured_image.image.get_thumbnail_url(),
        'tag': 'not-breaking'
        }
    subscriptions = Subscription.objects.all()
    for sub in subscriptions:
        try:
            webpush(
                subscription_info={
                    "endpoint": sub.endpoint,
                    "keys": {
                        "p256dh": sub.p256dh,
                        "auth": sub.auth
                    }},
                data=json.dumps(data),
                vapid_private_key="Mp2OSApC5ZQ11iHtKfTfAWycrr-YYl9yphpkeqKIy9E",
                vapid_claims={
                        "sub": "mailto:YourNameHere@example.org===",
                    }
            )
        except WebPushException as ex:
            sub.delete()

# Setup cron jobs

# 8:30 am
@kronos.register('29 8 * * *')
def push_morning():
    notification = Notification.objects.all().order_by('created_at').first()

    if notification is not None:
        push_notifications(notification.article)
        notification.delete()
    return

# 12:00 pm
@kronos.register('0 12 * * *')
def push_noon():
    notification = Notification.objects.all().order_by('created_at').first()

    if notification is not None:
        push_notifications(notification.article)
        notification.delete()
    return

# 5:30 pm
@kronos.register('29 5 * * *')
def push_afternoon():
    notification = Notification.objects.all().order_by('created_at').first()

    if notification is not None:
        push_notifications(notification.article)
        notification.delete()
    return