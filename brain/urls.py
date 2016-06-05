from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings
import views


urlpatterns=patterns('',
    url(r'', views.BrainView.as_view(), name='brain'),
#    url(r'^results/$', views.HeroDetail.as_view(), name='results'),      
    )

