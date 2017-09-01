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

STATICFILES_DIRS += (
    os.path.join(os.path.dirname(__file__), 'static/dist'),
)

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
