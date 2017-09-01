import os

from dispatch.default_settings import *

BASE_URL = 'https://ubyssey-prd.appspot.com/'

SECRET_KEY = os.environ.get('SECRET_KEY')

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
        'HOST': os.environ.get('SQL_HOST'),
        'NAME': os.environ.get('SQL_DATABASE'),
        'USER': os.environ.get('SQL_USER'),
        'PASSWORD': os.environ.get('SQL_USER'),
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

STATICFILES_DIRS += (
    os.path.join(os.path.dirname(__file__), 'static/dist'),
)

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
