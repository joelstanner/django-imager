from django.shortcuts import render
from profiles.models import ImagerProfile
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def library(request):

    return render(request,
                  'imager_images/library.html',
                  {'profile': ImagerProfile.objects.get(pk=request.user.id)})

@login_required
def stream(request):

    profile = ImagerProfile.objects.get(pk=request.user.id)
    following = profile.following()
    recent_pics = profile.photo_set.all()
    following_pics = []
    for followed in following:
        following_pics.append(followed.show_photos().order_by('date_uploaded'))
    return render(request,
                  'imager_images/profilestream.html',
                  {
                    'Profile': profile,
                    'Profile_pics': recent_pics,
                    'Following_pics': following_pics
                  })
