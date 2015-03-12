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
    return render(request,
                  'imager_images/profilestream.html',
                  {
                    'Photos': ImagerProfile.objects.all()[pk].show_photos(),
                    'Albums': ImagerProfile.objects.all()[pk].show_albums(),
                    'Profile': ImagerProfile.objects.all()[pk]
                  })
