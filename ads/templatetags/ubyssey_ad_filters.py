from django import template
from django.template.defaultfilters import stringfilter
from django.template.loader import render_to_string

register = template.Library()

MAX_ADS = 5 # based on the max number of "Intra_Article_X" slots available in Google Ad Manager
PARAGRAPHS_PER_AD = 6

@register.filter(name='inject_ads')
@stringfilter
def inject_ads(value, is_mobile):
    # Inspired by https://timonweb.com/django/creating-custom-template-filter-that-injects-adsense-ad-code-after-n-paragraph-in-django/ but heavily modified
    
    if not isinstance(is_mobile,bool):
        # If something goes wrong in detecting whether the user is on mobile or not, sensible failsafe is to assume they ARE
        # Doing so will cause the ads displayed to appear as "box" rather than "banner" size. Both work fine on desktop. Only box works well on mobile.
        is_mobile = True

    # Break down content into paragraphs
    paragraphs = value.split("</p>")

    if PARAGRAPHS_PER_AD < len(paragraphs): # If the article is somehow too short for even one ad, it doesn't get any
        x = range(0, len(paragraphs), PARAGRAPHS_PER_AD)
        for n in x:
            if n > 0: # Don't put an ad at the very beginning of the article                
                if (n // PARAGRAPHS_PER_AD) > MAX_ADS: # if we're above the max number of ads per article, stop!
                    break

                dfp = 'Intra_Article_' + str((n // PARAGRAPHS_PER_AD))
                div_id = dfp
                if is_mobile:
                    size = 'box'
                else:
                    size = 'banner'
                ad_context = {
                    'div_id' : div_id,
                    'dfp' : dfp,
                    'size' : size,
                }
                ad_string = render_to_string('ads/advertisement_inline.html', context=ad_context)
                paragraphs[n] = ad_string + paragraphs[n]

        # Assemble our text back with injected HTML
        value = "</p>".join(paragraphs)
    return value


