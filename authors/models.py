from django.db import models
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

class AllAuthorsPage(Page):
    subpage_types = [
        'authors.AuthorPage',
    ]
    parent_page_types = [
        'home.HomePage',
    ]
    max_count_per_parent = 1


class AuthorPage(Page):
    # The odd pattern used here was taken from: https://stackoverflow.com/questions/48625770/wagtail-page-title-overwriting
    # This is to treat the full_name as the "title" field rather than the usual Wagtail pattern of 
    parent_page_types = [
        'authors.AllAuthorsPage',
    ]

    full_name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    image = models.ForeignKey(
        "images.UbysseyImage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    ubyssey_role = models.CharField(
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
    content_panels = [
        # title not present, title should NOT be directly editable
        FieldPanel("full_name"),
        MultiFieldPanel(
            [
                ImageChooserPanel("image"),
                FieldPanel("facebook_url"),
                FieldPanel("twitter_url"),
            ],
            heading="Optional Stuff",
        ),
    ]

    def clean(self):
        """Override the values of title and slug before saving."""
        super().clean()
        self.title = self.full_name
        self.slug = slugify(self.full_name)  # slug MUST be unique & slug-formatted


    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        # indexes = [
        #     models.Index(fields=['article_authors','slug',]),
        # ]

# set a default blank slug for when the editing form renders
# we set this after the model is declared
AuthorPage._meta.get_field('slug').default = 'default-blank-slug'
