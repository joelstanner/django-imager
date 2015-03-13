from django.shortcuts import render
from imager_images.models import Photo
from profiles.models import ImagerProfile

def home(request):
    try:
        return render(
            request,
            'index.html',
            {'random_photo': Photo.random_image.all()[0].photo.url}
            )
    except IndexError:
        return render(
            request,
            'index.html',
            {'random_photo': '/media/default_stock_photo_640_360.jpg'}
            )

def profile(request):
    prof = ImagerProfile.objects.get(pk=request.user.id)
    print prof.show_all_albums()
    return render(request, 'profile.html', {'profile': ImagerProfile.objects.get(pk=request.user.id)})
