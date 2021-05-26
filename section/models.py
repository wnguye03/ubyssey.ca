from django.db import models

# Create your models here.

from wagtail.core.models import Page, Orderable

class SectionPage(models.Page):
    template = 'section/section.html'
    subpage_types = [
        'article.ArticlePage',
    ]

    