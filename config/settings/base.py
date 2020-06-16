"""
base.py, default settings, originating from Dispatch module.
Use: place .env file containing app configuration in /ubyssey.ca/

Part of the 12factor app philosophy is to keep config seperate from code. Typically, the environment variables are used for the config.
This code's primary job therefore ought to be retrieving the config from the environment rather than hardcoding in config settings.

Having these imported from Dispatch is too "magical" to be desirable, even if Dispatch is an explict dependency.
Don't Repeat Yourself, yes, but "redundancy" isn't bad if it's accross what are nominally entirely different projects!
More Pythonic is: Explicit rather than implicit.

Environment variable stuff is based on the following document from Google CodeLabs
https://codelabs.developers.google.com/codelabs/cloud-run-django/index.html?index=..%2F..index#5
"""

import os
import sys
import environ
from dispatch.apps import DispatchConfig


PROJECT_DIR = environ.Path(__file__) - 3 # i.e. the /ubyssey.ca directory
DISPATCH_APP_DIR = DispatchConfig.path

env_file = os.path.join(PROJECT_DIR, '.env') # Look for the environment variables file in the project directory

#If we didn't find an .env file, we try to make one using values stored in Google Cloud project. This requires authentication.
if not os.path.isfile('.env'): #TODO: does this ever return true?
    import google.auth
    from google.cloud import secretmanager as sm

    try:
        _, project = google.auth.default() #Will fail without GOOGLE_APPLICATION_CREDENTIALS

        if project:
            client = sm.SecretManagerServiceClient()
            path = client.secret_version_path(project, "django_settings", "latest") #TODO: UPDATE THIS LINE!!! taken
            payload = client.access_secret_version(path).payload.data.decode("UTF-8")
            with open(env_file, "w") as f:
                f.write(payload)
        else:
            sys.stderr.write("Error: No .env file or Google application credentials found!\n")      
    except Exception as e:       
        sys.stderr.write("Error in trying to generate .env file using Google application credentials!\n")

# We now have an .env file, so we need to get 
env = environ.Env(
    #set casting and defaults for config vars which are to be read from environment
    ORGANIZATION_NAME = (str, 'Ubyssey'),
    DEBUG=(bool,False),
    VERSION=(str,'0.0.0'),
    USE_TZ=(bool,True),
    TIME_ZONE=(str,'America/Vancouver'),
    STATIC_URL = (str,'/static/'),
    MEDIA_URL = (str,'/media/'),
    ROOT_URLCONF = (str,'ubyssey.urls'),
    DATABASE_URL = (str, 'mysql://root:ubyssey@db:3306/ubyssey'), # Toy "example" setting. Should only be used in dev environment, if anywhere
)
environ.Env.read_env(env_file)  # reading .env file.

# Setting Django's configs to the values taken from the .env file (or else to their defaults listed above)
ORGANIZATION_NAME = env('ORGANIZATION_NAME')
VERSION = env('VERSION')
DEBUG = env('DEBUG')
USE_TZ = env('USE_TZ')
TIME_ZONE = env('TIME_ZONE')
STATIC_URL = env('STATIC_URL')
MEDIA_URL = env('MEDIA_URL')
ROOT_URLCONF = env('ROOT_URLCONF')

# Initialize the databases
DATABASES = {'default': env.db('DATABASE_URL')}
# Note this use of the env object different from the other configs.
# If we assume DATABASE_URL is the toy example URL set above,
# env.db('DATABASE_URL') will parse it into a dictionary as illustrated below.
# This line therefore abbreviates how you may see databases set up in other Django projects
#
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'ubyssey',
#        'USER': 'root',
#        'PASSWORD': 'ubyssey',
#        'HOST': 'db',
#        'PORT': '3306',
#    },
#}

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
        'NAME': 'dispatch',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
			DISPATCH_APP_DIR('templates')
        ],
    },
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
    DISPATCH_APP_DIR('static/manager/dist')
]

GS_LOCATION = None
GS_STORAGE_BUCKET_NAME = None
GS_USE_SIGNED_URLS = False

PHONENUMBER_DB_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = 'CA'

PASSWORD_RESET_TIMEOUT_DAYS = 1
