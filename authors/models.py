from django.db import models
from django_extensions.db.fields import AutoSlugField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

@register_snippet
class AuthorSnippet(models.Model):
    full_name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    slug = AutoSlugField(
        populate_from="full_name",
        primary_key=True,
        unique=True,
        blank=False,
        null=False,
        max_length=255,
        editable=True,
    )

    # # This implementation represents an "easy" way to implement this which is analogous to how Dispatch did it, though less user-friendly than the alternative
    # image = models.ImageField(
    #     upload_to='images',
    #     null=True,
    #     blank=True,
    # )
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    title = models.CharField(
        max_length=255,
        null=False,
        blank=True,
        default='',
    )
    facebook_url = models.URLField(
        null=True,
        blank=True,
    )
    twitter_url = models.URLField(
        null=True,
        blank=True,
    )
    # For editting in wagtail:
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("slug"),
                FieldPanel("full_name"),
            ],
            heading="Essentials",
        ),
        MultiFieldPanel(
            [
                ImageChooserPanel("image"),
                FieldPanel("title"),
                FieldPanel("facebook_url"),
                FieldPanel("twitter_url"),
            ],
            heading="Optional Stuff",
        ),
    ]

    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
