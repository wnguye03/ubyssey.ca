from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField

# Create your models here.

class HomePage(Page):
    template = "home/home_page.html"

    # content = StreamField(
    #     [

    #     ]
    # )