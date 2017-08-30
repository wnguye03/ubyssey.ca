from dispatch.theme import register
from dispatch.theme.templates import Template
from dispatch.apps.frontend.fields import TextField, ModelField, SelectField

@register.template
class Default(Template):
    id = 'default'
    name = 'Default'

    IMAGE_SIZE_OPTIONS = (
        ('default', 'Default'),
        ('full', 'Full')
    )

    fields = (
        ('image_size', 'Image Size', SelectField(options=IMAGE_SIZE_OPTIONS)),
    )

@register.template
class Blank(Template):
    id = 'blank'
    name = 'Blank'

    fields = ()

@register.template
class FullWidth(Template):
    id = 'fw-story'
    name = 'Full width story'

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

@register.template
class Guide(Template):
    id = 'guide-to-ubc'
    name = 'Guide to UBC'

    fields = (
        ('subheading', 'Sub-heading', TextField()),
        ('intro', 'Intro text', TextField()),
        ('next_a', 'Up next A', TextField()),
        ('next_b', 'Up next B', TextField())
    )

@register.template
class Magazine(Template):
    id = 'magazine'
    name = 'Magazine - Article'

    COLOR_OPTIONS = (
        ('green', 'Green'),
        ('pink', 'Pink'),
        ('blue', 'Blue')
    )

    fields = (
        ('byline', 'Byline', TextField()),
        ('byline_2', 'Byline 2', TextField()),
        ('description', 'Description', TextField()),
        ('color', 'Accent Color', SelectField(options=COLOR_OPTIONS)),
    )

@register.template
class MagazinePoem(Template):
    id = 'magazine-poem'
    name = 'Magazine - Poem'

    fields = (
        ('byline', 'Byline', TextField()),
        ('byline_2', 'Byline 2', TextField()),
        ('top_color', 'Top Color', TextField()),
        ('bottom_color', 'Bottom Color', TextField()),
        ('text_color_a', 'Text Color A', TextField()),
        ('text_color_b', 'Text Color B', TextField()),
        ('offset', 'Top Offset', TextField()),
    )
