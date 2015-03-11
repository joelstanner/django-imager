from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', views.home, name='home_page'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/profile', views.home, name='home'),
    url(r'^foo/', include('profiles.urls'))
)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
