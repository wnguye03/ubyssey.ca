from dbtemplates.models import Template as DBTemplate

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)

class DBTemplateAdmin(ModelAdmin):
    model = DBTemplate
    menu_label = 'Custom HTML'
    menu_icon = 'code'
    menu_order = 800
    list_display = ('name',)
modeladmin_register(DBTemplateAdmin)