from django.conf.urls import url

from .import views

app_name = 'blog'
urlpatterns = [
    #类
    url(r'^$',views.index,name='index'),#首页函数
    url(r'^post/(?P<pk>[0-9]+)/$',views.PostDetaiIView.as_view(),name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$',views.CategoryView.as_view(),name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
    #函数
    # url(r'^$',views.IndexView.as_view(),name='index'),
    # url(r'^search/$',views.search,name='search'),
    # url(r'category/(?P<pk>[0-9]+)/$',views.category,name='category'),
    # url(r'^post/(?P<pk>[0-9]+)/$',views.detail,name='detail'),
    # url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
]