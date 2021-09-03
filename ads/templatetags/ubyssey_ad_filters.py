from django import template
from django.template.defaultfilters import stringfilter
from django.template.loader import render_to_string

register = template.Library()

@register.filter(name='inject_ads_after_paragraphs')
@stringfilter
def inject_ads_after_paragraphs(value, arg):
    # Inspired by https://timonweb.com/django/creating-custom-template-filter-that-injects-adsense-ad-code-after-n-paragraph-in-django/ but heavily modified
    
    if isinstance(arg,int):
        paragraphs_per_ad = arg
    else:
        paragraphs_per_ad = 6

    # Break down content into paragraphs
    paragraphs = value.split("</p>")

    if paragraphs_per_ad < len(paragraphs): # If the article is somehow too short for even one ad, it doesn't get any
        x = range(0, len(paragraphs), paragraphs_per_ad)
        for n in x:
            if n > 0: # Don't put an ad at the very beginning of the article
                # Append our code before the following paragraph
                paragraphs[n] = '<h2>AD GO HERE</h2>' + paragraphs[n]

        # Assemble our text back with injected adsense code
        value = "</p>".join(paragraphs)
    return value


