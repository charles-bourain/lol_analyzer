from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings
from items import views

urlpatterns=patterns('',
    url(r'^list/$', views.ItemList.as_view(), name='item_list'),
    # url(r'^detail/(?P<riot_id>[\w-]+)/$', views.HeroDetail.as_view(), name='item_detail'),      
    )

