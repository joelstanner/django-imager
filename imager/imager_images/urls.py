from django.conf.urls import patterns, url
from imager_images import views

urlpatterns = patterns('',
    url(r'^library/(?P<pk>\d+)$', views.library, name='profile-library'),
    url(r'^stream/(?P<pk>\d+)$', views.stream, name='profile-stream')
    )