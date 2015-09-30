from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', views.home, name='home_page'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^profiles/', include('profiles.urls')),
    url(r'^images/', include('imager_images.urls')),
)

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
