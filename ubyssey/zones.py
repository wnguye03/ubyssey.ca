from dispatch.theme import register
from dispatch.theme.widgets import Zone

@register.zone
class ArticleSidebar(Zone):
  id = 'article-sidebar'
  name = 'Article Sidebar'

@register.zone
class HomePageSidebar(Zone):
    id = 'homepage-sidebar'
    name = 'Homepage Sidebar'

@register.zone
class HomePageSidebarBottom(Zone):
    id = 'homepage-sidebar-bottom'
    name = 'Homepage Sidebar Bottom'

@register.zone
class ArticleHorizontal(Zone):
    id = 'article-horizontal'
    name = 'Article Horizontal'

@register.zone
class HomePageTakeover(Zone):
    id = 'homepage-takeover'
    name = 'Homepage Takeover'
