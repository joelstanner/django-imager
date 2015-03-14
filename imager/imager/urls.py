from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', views.home, name='home_page'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/profile/$', views.profile, name='profile'),
    url(r'^images/', include('imager_images.urls')),
    url(r'^add_photo/', views.PhotoCreate.as_view(
        template_name="photo_form.html",
        success_url='/images/library'),
        name='add_photo'),
    url(r'^add_album/', views.AlbumCreate.as_view(
        template_name="albums_form.html",
        success_url='/images/library'),
        name='add_album'),
    url(r'^update_album/(?P<pk>\d+)/$', views.AlbumUpdate.as_view(
        template_name="update_album.html",
        success_url='/images/library'),
        name='update_album'), 
    url(r'^update_photo/(?P<pk>\d+)/$', views.PhotoUpdate.as_view(
        template_name="update_photo.html",
        success_url='/images/library'),
        name='update_photo'),  
)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
