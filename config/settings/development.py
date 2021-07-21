# development.py, settings file
# see https://djangostars.com/blog/configuring-django-settings-best-practices/

# Two Scoops of Django, p. 47: "For the singular case of Django setting modules we want to override all the namespace"
# Therefore the below "import *" is correct
from .base import *

BASE_URL = 'http://localhost:8000/'

ALLOWED_HOSTS = ['localhost', '*']

INTERNAL_IPS = ['127.0.0.1', '0.0.0.0', 'localhost']

# Easily manipulable file cache for proof of concept for front page etc.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/workspaces/ubyssey.ca/cache/"
    }
}

MIDDLEWARE += [
    # other middlewares...
    'django_user_agents.middleware.UserAgentMiddleware',
]

TEMPLATES += [
{
        'NAME': 'ubyssey',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
			BASE_DIR('ubyssey/templates/')
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    }
]

# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

GCS_CREDENTIALS_FILE = '../gcs-local.json'

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

GCS_CREDENTIALS_FILE = '../gcs-local.json'

# Use in-memory file handler on Google App Engine
FILE_UPLOAD_HANDLERS = ['django.core.files.uploadhandler.MemoryFileUploadHandler',]
FILE_UPLOAD_MAX_MEMORY_SIZE = 25621440
