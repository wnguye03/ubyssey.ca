import os

# from ubyssey.secrets import Secrets
from google.cloud import datastore
client = datastore.Client()

from dispatch.default_settings import *

BASE_URL = 'https://www.ubyssey.ca/'
CANONICAL_DOMAIN = 'www.ubyssey.ca'

SECRET_KEY = client.get(client.key('Secrets', 'SECRET_KEY')).value
NOTIFICATION_KEY = client.get(client.key('Secrets', 'NOTIFICATION_KEY')).value

VERSION = '1.5.26'

ALLOWED_HOSTS = [
    'ubyssey.ca',
    'www.ubyssey.ca',
    'ubyssey-prd.appspot.com',
]

INSTALLED_APPS += [
    'ubyssey',
    'ubyssey.events',
    'django_user_agents',
]

ROOT_URLCONF = 'ubyssey.urls'

USE_TZ = True

TIME_ZONE = 'America/Vancouver'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': client.get(client.key('Secrets', 'SQL_HOST')).value,
        'NAME': client.get(client.key('Secrets', 'SQL_DATABASE')).value,
        'USER': client.get(client.key('Secrets', 'SQL_USER')).value,
        'PASSWORD': client.get(client.key('Secrets', 'SQL_PASSWORD')).value,
        'PORT': 3306,
    }
}

TEMPLATES += [
    {
        'NAME': 'ubyssey',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(os.path.dirname(__file__), 'templates'),
        ]
    }
]

SESSION_ENGINE = 'gae_backends.sessions.cached_db'
CACHES = {
    'default': {
        'BACKEND': 'gae_backends.memcache.MemcacheCache',
    }
}

MIDDLEWARE_CLASSES += [
    'google.appengine.ext.ndb.django_middleware.NdbDjangoMiddleware',
    'canonical_domain.middleware.CanonicalDomainMiddleware',
]

# GCS File Storage
DEFAULT_FILE_STORAGE = 'django_google_storage.storage.GoogleStorage'

GS_ACCESS_KEY_ID = client.get(client.key('Secrets', 'GS_ACCESS_KEY_ID')).value
GS_SECRET_ACCESS_KEY = client.get(client.key('Secrets', 'GS_SECRET_ACCESS_KEY')).value
GS_STORAGE_BUCKET_NAME = 'ubyssey'
GS_LOCATION = 'media'
GS_USE_SIGNED_URLS = True
GS_QUERYSTRING_AUTH = False

STATICFILES_DIRS += (
    os.path.join(os.path.dirname(__file__), 'static/dist'),
)

STATIC_URL = 'https://ubyssey.storage.googleapis.com/static/'
MEDIA_URL = 'https://ubyssey.storage.googleapis.com/media/'

# Facebook
FACEBOOK_CLIENT_ID = client.get(client.key('Secrets', 'FACEBOOK_CLIENT_ID')).value
FACEBOOK_CLIENT_SECRET = client.get(client.key('Secrets', 'FACEBOOK_CLIENT_SECRET')).value

EMAIL_HOST = client.get(client.key('Secrets', 'EMAIL_HOST')).value
EMAIL_PORT = 465
EMAIL_HOST_USER = client.get(client.key('Secrets', 'EMAIL_HOST_USER')).value
EMAIL_HOST_PASSWORD = client.get(client.key('Secrets', 'EMAIL_HOST_PASSWORD')).value
EMAIL_USE_SSL = True

UBYSSEY_ADVERTISING_EMAIL = client.get(client.key('Secrets', 'UBYSSEY_ADVERTISING_EMAIL')).value

# Use in-memory file handler on Google App Engine
FILE_UPLOAD_HANDLERS = ['django.core.files.uploadhandler.MemoryFileUploadHandler',]
FILE_UPLOAD_MAX_MEMORY_SIZE = 25621440
