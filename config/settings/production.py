# production.py , Django settings file
# Two Scoops of Django, p. 47: "For the singular case of Django setting modules we want to override all the namespace"
# Therefore the below "import *" is correct
from .base import *
from google.oauth2 import service_account

import environ

env = environ.Env() #Scope issues without this line?

BASE_URL = 'https://www.ubyssey.ca/'

ALLOWED_HOSTS = ['localhost', '*']

INTERNAL_IPS = ['127.0.0.1', '0.0.0.0', 'localhost']

INSTALLED_APPS += [
]

# Sessions are used to anonymously keep track of individual site visitors
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Caches are used to store the results of SQL queries so it can be quickly retrieved and needs to do less work
# The cache requires a Memcached instance be set up in Google Cloud Platform (GCP) and access connectors to be set both on GCP and in app.yaml
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        # 'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        # 'LOCATION': '10.18.240.4:11211',
    }
}

MIDDLEWARE += [
    'canonical_domain.middleware.CanonicalDomainMiddleware',
]

ADS_TXT_URL = 'https://ubyssey.storage.googleapis.com/ads.txt'

# GCS File Storage - Production Only
MEDIA_URL = 'https://ubyssey.storage.googleapis.com/media/'
MEDIA_ROOT = ''
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_ACCESS_KEY_ID = env('GS_ACCESS_KEY_ID')
GS_SECRET_ACCESS_KEY = env('GS_SECRET_ACCESS_KEY')
# GS_CREDENTIALS = service_account.Credentials.from_service_account_file('ubyssey-prd-ee6290e6327f.json')
# GS_CREDENTIALS = env('GOOGLE_APPLICATION_CREDENTIALS')
GS_STORAGE_BUCKET_NAME = 'ubyssey' # See documentation https://django-storages.readthedocs.io/en/latest/backends/gcloud.html
GS_BUCKET_NAME = GS_STORAGE_BUCKET_NAME # https://github.com/mirumee/saleor/issues/5222 see suggestion both these variables are needed
GS_LOCATION = 'media'
GS_USE_SIGNED_URLS = True
GS_QUERYSTRING_AUTH = False
GS_FILE_OVERWRITE = False

# Facebook - Production Only
FACEBOOK_CLIENT_ID = env('FACEBOOK_CLIENT_ID')
FACEBOOK_CLIENT_SECRET = env('FACEBOOK_CLIENT_SECRET')

# Emails - Production Only
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = 465
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True
UBYSSEY_ADVERTISING_EMAIL = env('UBYSSEY_ADVERTISING_EMAIL')

# Use in-memory file handler on Google App Engine
FILE_UPLOAD_HANDLERS = ['django.core.files.uploadhandler.MemoryFileUploadHandler',]
FILE_UPLOAD_MAX_MEMORY_SIZE = 25621440

ADMINS = [
	('Keegan', 'k.landrigan@ubyssey.ca'),
]
