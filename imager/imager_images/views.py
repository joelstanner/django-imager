from django.shortcuts import render
from profiles.models import ImagerProfile

# Create your views here.
def library(request, pk):
    pk = int(pk)
    return render(request,
                  'imager_images/library.html',
                  {
                    'Photos': ImagerProfile.objects.get(pk=pk).show_photos(),
                    'Albums': ImagerProfile.objects.get(pk=pk).show_albums(),
                    'Profile': ImagerProfile.objects.get(pk=pk)
                  })

def stream(request, pk):
    pk = int(pk)
    profile = ImagerProfile.objects.get(pk=pk)
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
