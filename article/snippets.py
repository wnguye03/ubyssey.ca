from django.db import models
# from wagtail.admin.edit_handlers import (
#     FieldPanel,
#     StreamFieldPanel,
#     MultiFieldPanel,
# )
from wagtail.snippets.models import register_snippet

from dispatch.models import Article

@register_snippet
class DispatchCounterpartSnippet(models.Model):
    dispatch_version = models.ForeignKey(
        Article,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
    )
