import  xadmin

from .models import EmailVerifyRecord, Banner, UserProfile
from xadmin.plugins.auth import UserAdmin
from xadmin import views
from xadmin.layout import Fieldset,Main,Side,Row





class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSetting(object):
    site_title = "达内后台管理系统"
    site_footer = "aid1805"
    menu_style = "accordion"

#xadmin中这里是继承object，不再是继承admin
class EmailVerifyRecordAdmin(object):
    # 显示的列
    list_display = ['code', 'email', 'send_type', 'send_time']
    # 搜索的字段
    search_fields = ['code', 'email', 'send_type']
    # 过滤
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-address-book-o'


class BannerAdmin(object):
    list_display = ['title', 'image', 'url','index', 'add_time']
    search_fields = ['title', 'image', 'url','index']
    list_filter = ['title', 'image', 'url','index', 'add_time']
    model_icon = 'fa fa-area-chart'





xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)
