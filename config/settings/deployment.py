# deployment.py, Django settings file

# Two Scoops of Django, p. 47: "For the singular case of Django setting modules we want to override all the namespace"
# Therefore the below "import *" is correct
from .base import *

SECRET_KEY = 'TEMP-KEY'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += ['ubyssey.events',]

STATICFILES_DIRS += [
    PROJECT_DIR('ubyssey/static/dist'),
]

STATIC_ROOT = '/home/travis/build/ubyssey/ubyssey.ca/gcs/static'