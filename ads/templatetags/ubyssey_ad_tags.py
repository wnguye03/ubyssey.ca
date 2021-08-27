from django import template
from ..models import AdSlot

register = template.Library()

@register.inclusion_tag('ads/advertisement.html')
def adslot(slug) -> dict:
    try:
        ad_slot = AdSlot.objects.get(slug=slug)
        return {
            'div_id' : ad_slot.div_id,
            'dfp' : ad_slot.dfp,
            'size' : ad_slot.size,
            'div_class' : ad_slot.div_class,
        }
    except:
        return {
            'div_id' : 'ad-tag-error',
            'dfp' : 'ad-tag-error',
            'size' : 'ad-tag-error',
            'div_class' : '',
        }