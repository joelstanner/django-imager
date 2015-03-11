from django.conf.urls import patterns, url
from profiles import views
from views import ProfileDetailView

urlpatterns = patterns('',
    url(r'^$', views.profile_home, name='profile_home'),
    url(r'^(?P<pk>\d+)$', ProfileDetailView.as_view(), name='profile-detail')
    )