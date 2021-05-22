"""
See: https://docs.wagtail.io/en/stable/advanced_topics/images/custom_image_model.html
"""

from django.db import models
from django.db.models.fields.related import ForeignKey
from wagtail.images.models import Image, AbstractImage, AbstractRendition


class UbysseyImage(AbstractImage):
    # Add any extra fields to image here

    # eg. To add a caption field:
    # caption = models.CharField(max_length=255, blank=True)
    author = models.ForeignKey(
        "authors.AuthorSnippet",
        null=True,
        on_delete=models.SET_NULL
    )

    admin_form_fields = Image.admin_form_fields + (
        # Then add the field names here to make them appear in the form:
        # 'caption',
        'author',
    )

class UbysseyRendition(AbstractRendition):
    image = models.ForeignKey(UbysseyImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )