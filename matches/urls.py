from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings
from matches import views

urlpatterns=patterns('',
    url(r'^matchtest/$', views.MatchTest.as_view(), name='match_test'),
    # url(r'^detail/(?P<riot_id>[\w-]+)/$', views.HeroDetail.as_view(), name='item_detail'),      
    )

