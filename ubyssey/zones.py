from dispatch.theme import register
from dispatch.theme.widgets import Zone

@register.zone
class EventSidebar(Zone):
    id = 'event-sidebar'
    name = 'Event Sidebar'

@register.zone
class HomePageSidebar(Zone):
    id = 'homepage-sidebar'
    name = 'Homepage Sidebar'
