import re as regex
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_youtube_url(value):
    """
    Matches value against the regular expression:
    (https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})

    :param value: should be a Youtube URL in string form
    :raises ValidationError: error when regex fails to match
    """
    youtube_regex = regex.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')

    if not youtube_regex.match(value):
        raise ValidationError(
            _('%(value)s is not a valid youtube URL'),
            params={'value': value},
        )
