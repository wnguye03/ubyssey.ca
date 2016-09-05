from dispatch.apps.frontend.helpers import templates
from dispatch.apps.frontend.templates import BaseTemplate
from dispatch.apps.frontend.fields import TextField, ModelField, SelectField

class Default(BaseTemplate):

    NAME = 'Default'
    SLUG = 'default'

    IMAGE_SIZE_OPTIONS = (
        ('default', 'Default'),
        ('full', 'Full')
    )

    fields = (
        ('image_size', 'Image Size', SelectField(options=IMAGE_SIZE_OPTIONS)),
    )

class FullWidth(BaseTemplate):

    NAME = 'Full width story'
    SLUG = 'fw-story'

    IMAGE_SIZE_OPTIONS = (
        ('default', 'Default'),
        ('full', 'Full')
    )

    HEADER_LAYOUT_OPTIONS = (
        ('right-image', 'Right Image'),
        ('top-image', 'Top Image'),
        ('banner-image', 'Banner Image')
    )

    fields = (
        ('description', 'Description', TextField()),
        ('image_size', 'Image Size', SelectField(options=IMAGE_SIZE_OPTIONS)),
        ('header_layout', 'Header Layout', SelectField(options=HEADER_LAYOUT_OPTIONS))
    )

class Guide(BaseTemplate):

    NAME = 'Guide to UBC'
    SLUG = 'guide-to-ubc'

    fields = (
        ('subheading', 'Sub-heading', TextField()),
        ('intro', 'Intro text', TextField())
    )

templates.register(Default)
templates.register(FullWidth)
templates.register(Guide)
