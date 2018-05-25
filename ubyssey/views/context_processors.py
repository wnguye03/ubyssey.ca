import ubyssey
from django.conf import settings


def global_settings(request):
    return {
        'version': ubyssey.__version__
    }
