from django import template
from django.template.defaultfilters import stringfilter
from django.template.loader import render_to_string

register = template.Library()

@register.filter(name='inject_ads')
@stringfilter
def inject_ads_after_paragraphs(value, arg):
    # Inspired by https://timonweb.com/django/creating-custom-template-filter-that-injects-adsense-ad-code-after-n-paragraph-in-django/ but heavily modified
    pass