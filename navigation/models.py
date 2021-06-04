from django.db import models
from django_extensions.db.fields import AutoSlugField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.core.models import Orderable
from wagtail.snippets.models import register_snippet

class NavigationMenuItem(Orderable):
    navigation_menu = ParentalKey(
        "navigation.NavigationMenu",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

#-----Snippet models-----
@register_snippet
class NavigationMenu(ClusterableModel):
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )
    slug = AutoSlugField(
        max_length=100,
        populate_from="name",
        null=False,
        blank=False,
        editable=True,
    )

    def __str__(self):
        return self.name
