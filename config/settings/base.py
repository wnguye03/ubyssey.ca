"""
base.py, default settings, originating from Dispatch module

Having these imported from Dispatch is too "magical" to be desirable, even if Dispatch is an explict dependency.
Don't Repeat Yourself, yes, but "redundancy" isn't bad if it's accross what are nominally entirely different projects!
More Pythonic is: Explicit rather than implicit.
"""

import os
import environ
import dispatch
PROJECT_DIR = environ.Path(__file__) - 3 # i.e. the /ubyssey.ca directory
DISPATCH_DIR = environ.Path(dispatch.apps.DispatchConfig.path)

ORGANIZATION_NAME = 'Dispatch'
VERSION = '1.6.34'

# Application definition
INSTALLED_APPS = [
    'dispatch.apps.DispatchConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'rest_framework',
    'rest_framework.authtoken'
]


# Replace default user model
AUTH_USER_MODEL = 'dispatch.User'

API_URL = '/api/'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Templates
TEMPLATES = [
    {
        'NAME': 'app_dirs',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
    {
        'NAME': 'ubyssey',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
			PROJECT_DIR('ubyssey/templates/')
        ],
    },
    {
        'NAME': 'dispatch',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            DISPATCH_DIR('templates')
        ],
    }
]

# REST framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'UNICODE_JSON': True,
    'PAGE_SIZE': 10,
    'DATETIME_INPUT_FORMATS': ['iso-8601']
}

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

STATICFILES_DIRS = [
    PROJECT_DIR('ubyssey/static'),
    DISPATCH_DIR('static')
]

GS_LOCATION = None
GS_STORAGE_BUCKET_NAME = None
GS_USE_SIGNED_URLS = False

PHONENUMBER_DB_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = 'CA'

PASSWORD_RESET_TIMEOUT_DAYS = 1
