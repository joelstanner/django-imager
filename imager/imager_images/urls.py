from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^library$', views.library, name='profile-library'),
    url(r'^stream$', views.stream, name='profile-stream'),
    url(r'^add_photo/', login_required(views.PhotoCreate.as_view(
        template_name="imager_images/create_form.html",
        success_url='/images/library')),
        name='add_photo'),
    url(r'^add_album/', login_required(views.AlbumCreate.as_view(
        template_name="imager_images/create_form.html",
        success_url='/images/library')),
        name='add_album'),
    url(r'^update_album/(?P<pk>\d+)/$', login_required(views.AlbumUpdate.as_view(
        template_name="imager_images/update_album.html",
        success_url='/images/library')),
        name='update_album'),
    url(r'^update_photo/(?P<pk>\d+)/$', login_required(views.PhotoUpdate.as_view(
        template_name="imager_images/update_photo.html",
        success_url='/images/library')),
        name='update_photo'),
    url(r'^delete_photo/(?P<pk>\d+)/$', login_required(views.PhotoDelete.as_view(
        template_name="imager_images/delete_form.html",
        success_url='/images/library')),
        name='delete_photo'),
    url(r'^delete_album/(?P<pk>\d+)/$', login_required(views.AlbumDelete.as_view(
        template_name="imager_images/delete_form.html",
        success_url='/images/library')),
        name='delete_album'),
    )