from django.conf.urls import patterns, url
from imager_images import views

urlpatterns = patterns('',
    url(r'^library$', views.library, name='profile-library')
    )