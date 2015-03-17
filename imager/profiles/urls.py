from django.conf.urls import patterns, url
import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', views.profile, name='profile'),
    url(r'^update_profile/(?P<pk>\d+)/$', login_required(views.ProfileUpdate.as_view(
        template_name="profiles/update_profile.html",
        success_url='/images/library')),
        name='update_profile'),
    )