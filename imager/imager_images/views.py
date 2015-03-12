from django.shortcuts import render
from profiles.models import ImagerProfile

# Create your views here.
def library(request, pk):
    pk = int(pk)
    return render(request,
                  'imager_images/library.html',
                  {
                    'Photos': ImagerProfile.objects.all()[pk].show_photos(),
                    'Albums': ImagerProfile.objects.all()[pk].show_albums(),
                    'Profile': ImagerProfile.objects.all()[pk]
                  })

def stream(request, pk):
    pk = int(pk)
    profile = ImagerProfile.objects.get(pk=pk)
    following = profile.following()
    recent_pics = profile.show_photos()
    following_pics = []
    for followed in following:
        following_pics.append(followed.show_photos())
    return render(request,
                  'imager_images/profilestream.html',
                  {
                    'Profile': profile,
                    'Profile_pics': recent_pics,
                    'Following_pics': following_pics
                  })
