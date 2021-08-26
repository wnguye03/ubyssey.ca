from .models import AdSlot
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)

class AdAdmin(ModelAdmin):
    model = AdSlot
    menu_label = 'Manage Ads'
    menu_icon = 'cogs'
    menu_order = 850
    list_display = ('slug', 'dfp', 'size','div_id')
modeladmin_register(AdAdmin)