# from dispatch.theme import register
# from dispatch.theme.widgets import Widget, Zone
# from dispatch.theme.fields import CharField, EventField
#
# from dispatch.apps.frontend.models import Zone as ZoneModel
# from dispatch.apps.content.models import Event as EventModel
#
# @register.zone
# class TestZone(Zone):
#     id = 'test-zone'
#     name = 'Test Zone'
#
# @register.widget
# class EventWidget(Widget):
#     id = 'event-widget'
#     name = 'Event widget'
#     template = 'widgets/event-widget.html'
#     zones = [TestZone]
#
#     title = CharField('Title')
#     event = EventField('Event')
#
# (zone, created) = ZoneModel.objects.get_or_create(zone_id='test-zone')
#
# zone.widget_id = 'event-widget'
#
# zone.data = {
#     'title': 'test title 2',
#     'event': 'event-widget'
# }
#
# zone.save()
