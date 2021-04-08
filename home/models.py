from django.db import models
from wagtail.core.models import Page

# Create your models here.

class HomePage(Page):
    template = "home/home_page.html"