from dispatch.models import Article
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_published_article(value):
    """
    Validator for Dispatch articles. Validates whether a slug corresponds to a Dispatch article

    Args:
        value (str): the slug to be checked
    """
    qs = Article.objects.filter(is_published=True, slug=value)
    if len(qs) < 1:
        raise ValidationError(
            _('%(value)s is not the slug of a published article!'),
            params={'value': value},
        )
