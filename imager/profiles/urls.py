from django.conf.urls import patterns, url
from profiles import views

urlpatterns = patterns('',
    url(r'^$', views.profile_home, name='profile_home'),
)