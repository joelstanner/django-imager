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
    url(r'^add_photo/', views.PhotoCreate.as_view(template_name="photo_form.html", success_url='/'), name='add_photo')
)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
