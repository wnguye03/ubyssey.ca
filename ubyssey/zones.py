from dispatch.theme import register
from dispatch.theme.widgets import Zone

@register.zone
class ArticleSidebar(Zone):
  id = 'article-sidebar'
  name = 'Article Sidebar'

@register.zone
class HomePageSidebarBottom(Zone):
    id = 'homepage-sidebar-bottom'
    name = 'Homepage Sidebar Bottom'

@register.zone
class ArticleHorizontal(Zone):
    id = 'article-horizontal'
    name = 'Article Horizontal'

@register.zone
class FrontPage(Zone):
    id = 'frontpage'
    name = 'FrontPage'

@register.zone
class WholeSiteBanner(Zone):
    id = 'whole-site-banner'
    name = 'Whole Site Banner'
