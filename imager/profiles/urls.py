from django.conf.urls import patterns, url
from profiles import views
from views import ProfileDetailView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)$', login_required(ProfileDetailView.as_view()), name='profile-detail')
    )