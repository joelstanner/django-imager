from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', views.home, name='home_page'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/profile/$', views.profile, name='profile'),
    url(r'^images/', include('imager_images.urls')),
    url(r'^update_profile/(?P<pk>\d+)/$', login_required(views.ProfileUpdate.as_view(
        template_name="update_profile.html",
        success_url='/images/library')),
        name='update_profile'),
    url(r'^add_photo/', login_required(views.PhotoCreate.as_view(
        template_name="create_form.html",
        success_url='/images/library')),
        name='add_photo'),
    url(r'^add_album/', login_required(views.AlbumCreate.as_view(
        template_name="create_form.html",
        success_url='/images/library')),
        name='add_album'),
    url(r'^update_album/(?P<pk>\d+)/$', login_required(views.AlbumUpdate.as_view(
        template_name="update_album.html",
        success_url='/images/library')),
        name='update_album'),
    url(r'^update_photo/(?P<pk>\d+)/$', login_required(views.PhotoUpdate.as_view(
        template_name="update_photo.html",
        success_url='/images/library')),
        name='update_photo'),
    url(r'^delete_photo/(?P<pk>\d+)/$', login_required(views.PhotoDelete.as_view(
        template_name="delete_photo.html",
        success_url='/images/library')),
        name='delete_photo'),
    url(r'^delete_album/(?P<pk>\d+)/$', login_required(views.AlbumDelete.as_view(
        template_name="delete_album.html",
        success_url='/images/library')),
        name='delete_album'),
)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
