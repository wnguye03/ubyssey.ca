from django.conf import settings
#from storages.backends.gs import GSBotoStorage
from django_google_storage.storage import GoogleStorage

class StaticStorage(GoogleStorage):
    location = settings.STATICFILES_LOCATION

class MediaStorage(GoogleStorage):
    location = settings.MEDIAFILES_LOCATION
