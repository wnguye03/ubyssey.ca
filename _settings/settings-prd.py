import os
from dispatch.default_settings import *
from google.cloud import datastore
client = datastore.Client()

BASE_URL = 'https://www.ubyssey.ca/'
CANONICAL_DOMAIN = 'www.ubyssey.ca'

query = client.query(kind='Secrets')
query.add_filter('key', '=', 'SECRET_KEY')
SECRET_KEY = list(query.fetch())[0].value

query.add_filter('key', '=', 'NOTIFICATION_KEY')
NOTIFICATION_KEY = list(query.fetch())[0].value

VERSION = '1.5.29'

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

query.add_filter('key', '=', 'SQL_HOST')
DB_HOST = list(query.fetch())[0].value

query.add_filter('key', '=', 'SQL_DATABASE')
DB_NAME = list(query.fetch())[0].value

query.add_filter('key', '=', 'SQL_USER')
DB_USER = list(query.fetch())[0].value

query.add_filter('key', '=', 'SQL_PASSWORD')
DB_PASSWORD = list(query.fetch())[0].value

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': DB_HOST,
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
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
    'canonical_domain.middleware.CanonicalDomainMiddleware',
]

# GCS File Storage
DEFAULT_FILE_STORAGE = 'django_google_storage.storage.GoogleStorage'

query.add_filter('key', '=', 'GS_ACCESS_KEY_ID')
GS_ACCESS_KEY_ID = list(query.fetch())[0].value

query.add_filter('key', '=', 'GS_SECRET_ACCESS_KEY')
GS_SECRET_ACCESS_KEY = list(query.fetch())[0].value

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
query.add_filter('key', '=', 'FACEBOOK_CLIENT_ID')
FACEBOOK_CLIENT_ID = list(query.fetch())[0].value

query.add_filter('key', '=', 'FACEBOOK_CLIENT_SECRET')
FACEBOOK_CLIENT_SECRET = list(query.fetch())[0].value

# Emails
query.add_filter('key', '=', 'EMAIL_HOST')
EMAIL_HOST = list(query.fetch())[0].value

EMAIL_PORT = 465

query.add_filter('key', '=', 'EMAIL_HOST_USER')
EMAIL_HOST_USER = list(query.fetch())[0].value

query.add_filter('key', '=', 'EMAIL_HOST_PASSWORD')
EMAIL_HOST_PASSWORD = list(query.fetch())[0].value

EMAIL_USE_SSL = True

query.add_filter('key', '=', 'UBYSSEY_ADVERTISING_EMAIL')
UBYSSEY_ADVERTISING_EMAIL = list(query.fetch())[0].value

# Use in-memory file handler on Google App Engine
FILE_UPLOAD_HANDLERS = ['django.core.files.uploadhandler.MemoryFileUploadHandler',]
FILE_UPLOAD_MAX_MEMORY_SIZE = 25621440
