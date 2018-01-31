from django.contrib import admin

# Register your models here.
from .models import Post,Tag,Category

import xadmin
from xadmin import views


class PostAdmin(object):
    list_display = ['title','create_time','modified_time','category','author']
    search_fields = ['title']

    list_filter = ['title','create_time','modified_time','category','author']
    model_icon = 'fa fa-address-card'


class BaseSettings(object):

    enable_themes =True
    use_bootswatch = True


class GloablSettings(object):
    site_title = '我的后台'
    site_footer = '我的底部'
    menu_style = 'accordion'

xadmin.site.register(views.CommAdminView,GloablSettings)

xadmin.site.register(views.BaseAdminView,BaseSettings)
xadmin.site.register(Post,PostAdmin)
xadmin.site.register(Category)
xadmin.site.register(Tag)