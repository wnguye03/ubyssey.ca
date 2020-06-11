# development.py, settings file
# see https://djangostars.com/blog/configuring-django-settings-best-practices/

# Two Scoops of Django, p. 47: "For the singular case of Django setting modules we want to override all the namespace"
# Therefore the below "import *" is correct
from .base import *

env = environ.Env()
environ.Env.read_env()  # reading .env file

BASE_URL = 'http://localhost:8000/'

SECRET_KEY = '&t7b#38ncrab5lmpe#pe#41coa-8ctwuy@tm0!x8*n_r38x_m*'
NOTIFICATION_KEY = "Mp2OSApC5ZQ11iHtKfTfAWycrr-YYl9yphpkeqKIy9E"

ALLOWED_HOSTS = ['localhost', '*']

INSTALLED_APPS += ['ubyssey.events', 'django_user_agents', ]

INTERNAL_IPS = ['127.0.0.1', 'localhost']

ROOT_URLCONF = 'ubyssey.urls'

MIDDLEWARE = (
    # other middlewares...
    'django_user_agents.middleware.UserAgentMiddleware',
)

DEBUG = True
USE_TZ = True

TIME_ZONE = 'America/Vancouver'

DATABASES = {'default': env.db('DATABASE_URL')}
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

TEMPLATES += [
 {
        'NAME': 'ubyssey',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
			PROJECT_DIR('ubyssey/templates/')
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    }
]

STATICFILES_DIRS += [
    PROJECT_DIR('ubyssey/static/dist'),
    PROJECT_DIR('service-workers'),
]

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

GCS_CREDENTIALS_FILE = '../gcs-local.json'

SERVICE_WORKER_URL = '/service-worker.js'

MEDIA_ROOT = PROJECT_DIR('media')

# Use in-memory file handler on Google App Engine
FILE_UPLOAD_HANDLERS = ['django.core.files.uploadhandler.MemoryFileUploadHandler',]
FILE_UPLOAD_MAX_MEMORY_SIZE = 25621440
