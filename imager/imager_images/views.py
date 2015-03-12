from django.shortcuts import render
from profiles.models import ImagerProfile

# Create your views here.
def library(request):
    return render(request,
                  'imager_images/library.html',
                  {
                    'Photos': ImagerProfile.objects.all()[2].show_photos(),
                    'Albums': ImagerProfile.objects.all()[2].show_albums(),
                    'Profile': ImagerProfile.objects.all()[2]
                  })
