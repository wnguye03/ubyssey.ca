from .models import AdSlot
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from wagtailmodelchooser import register_model_chooser

register_model_chooser(AdSlot)

class AdAdmin(ModelAdmin):
    model = AdSlot
    menu_label = 'Manage Ads'
    menu_icon = 'cogs'
    menu_order = 850
    list_display = ('slug', 'dfp', 'size','div_id','div_class')
modeladmin_register(AdAdmin)