from dispatch.theme import register
from dispatch.theme.widgets import Zone

@register.zone
class HomePageSidebar(Zone):
    id = 'homepage-sidebar'
    name = 'Homepage Sidebar'

@register.zone
class HomePageSidebarBottom(Zone):
    id = 'homepage-sidebar-bottom'
    name = 'Homepage Sidebar Bottom'
