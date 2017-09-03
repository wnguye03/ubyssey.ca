from django.conf import settings
from storages.backends.gs import GSBotoStorage

class StaticStorage(GSBotoStorage):
    location = settings.STATICFILES_LOCATION

class MediaStorage(GSBotoStorage):
    location = settings.MEDIAFILES_LOCATION
