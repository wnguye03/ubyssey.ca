"""
See: https://docs.wagtail.io/en/stable/advanced_topics/images/custom_image_model.html
"""

import os
from datetime import date
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils.translation import gettext_lazy as _
from wagtail.core.models import Orderable
from wagtail.core.utils import string_to_ascii
from wagtail.images.models import Image, AbstractImage, AbstractRendition


class UbysseyImage(AbstractImage):
    """
    Custom Image model for the Ubyssey

    Some fields are inhereted from AbstractImage. These are:
      title - main req
      file
      width
      height
      created_at
      uploaded_by_user
      tags - main req
      focal_point_x
      focal_point_y
      focal_point_width
      focal_point_height
      file_size
      file_hash
      objects
    """
    author = models.ForeignKey( #main req from original
        "authors.AuthorPage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    updated_at = models.DateTimeField(auto_now=True)

    legacy_filename = models.TextField(
        null=False,
        blank=True,
        default='',
    )

    admin_form_fields = Image.admin_form_fields + (
        'author',
    )

    def get_upload_to(self, filename):
        """
        Overrides original. Only difference is in folder_name
        Copied from:

        https://github.com/wagtail/wagtail/blob/main/wagtail/images/models.py
        """

        # If this were inheriting from ImageField, we'd just include the '%Y/%m' in the string
        # See https://docs.djangoproject.com/en/dev/ref/models/fields/#imagefield
        # Be careful of differances from ImageField!
        folder_name = 'wagtail_images/' + date.today().strftime('%Y/%m')
        filename = self.file.field.storage.get_valid_name(filename)

        # do a unidecode in the filename and then
        # replace non-ascii characters in filename with _ , to sidestep issues with filesystem encoding
        filename = "".join((i if ord(i) < 128 else '_') for i in string_to_ascii(filename))

        # Truncate filename so it fits in the 100 character limit
        # https://code.djangoproject.com/ticket/9893
        full_path = os.path.join(folder_name, filename)
        if len(full_path) >= 95:
            chars_to_trim = len(full_path) - 94
            prefix, extension = os.path.splitext(filename)
            filename = prefix[:-chars_to_trim] + extension
            full_path = os.path.join(folder_name, filename)

        return full_path
    
    class Meta(AbstractImage.Meta):
        verbose_name = _('Ubyssey image')
        verbose_name_plural = _('Ubyssey images')
        permissions = [
            ("choose_image", "Can choose image"),
        ]


class UbysseyRendition(AbstractRendition):
    """
    Custom Renditions model for the Ubyssey
    """
    image = models.ForeignKey(UbysseyImage, on_delete=models.CASCADE, related_name='renditions')
    def get_upload_to(self, filename):
        """
        Overrides original. Only difference is in folder_name Copried from:

        https://github.com/wagtail/wagtail/blob/main/wagtail/images/models.py
        """

        folder_name = 'wagtail_renditions/' + date.today().strftime('%Y/%m')
        filename = self.file.field.storage.get_valid_name(filename)
        return os.path.join(folder_name, filename)

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )