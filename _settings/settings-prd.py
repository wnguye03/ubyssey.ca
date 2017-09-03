import os

from ubyssey.secrets import Secrets

from dispatch.default_settings import *

BASE_URL = 'https://ubyssey-prd.appspot.com/'

SECRET_KEY = Secrets.get('SECRET_KEY')

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'ubyssey',
	'ubyssey.events',
]

ROOT_URLCONF = 'ubyssey.urls'

DEBUG = True
USE_TZ = True

TIME_ZONE = 'America/Vancouver'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': Secrets.get('SQL_HOST'),
        'NAME': Secrets.get('SQL_DATABASE'),
        'USER': Secrets.get('SQL_USER'),
        'PASSWORD': Secrets.get('SQL_USER'),
        'PORT': 3306,
    }
}

TEMPLATES += [
    {
        'NAME': 'ubyssey',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(os.path.dirname(__file__), 'templates'),
        ],
    }
]

# GCS File Storage
DEFAULT_FILE_STORAGE = 'ubyssey.custom_storages.MediaStorage'
STATICFILES_STORAGE = 'ubyssey.custom_storages.StaticStorage'

GS_ACCESS_KEY_ID = Secrets.get('GS_ACCESS_KEY_ID')
GS_SECRET_ACCESS_KEY = Secrets.get('GS_SECRET_ACCESS_KEY')
GS_STORAGE_BUCKET_NAME = 'ubyssey'

STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'

STATICFILES_DIRS += (
    os.path.join(os.path.dirname(__file__), 'static/dist'),
)

STATIC_URL = 'https://storage.googleapis.com/ubyssey/static/'
MEDIA_URL = 'https://storage.googleapis.com/ubyssey/media/'
