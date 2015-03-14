from django.shortcuts import render, redirect
from imager_images.models import Photo, Album
from profiles.models import ImagerProfile
from django.views.generic.edit import CreateView


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
    if not request.user.is_authenticated():
        print 'thing'
        return redirect('/accounts/login/')

    prof = ImagerProfile.objects.get(pk=request.user.id)
    print prof.show_all_albums()
    return render(request, 'profile.html', {'profile': ImagerProfile.objects.get(pk=request.user.id)})


class PhotoCreate(CreateView):
    model = Photo
    fields = ['title', 'description', 'published', 'photo', 'profile']


class AlbumCreate(CreateView):
    model = Album
    fields = ['title', 'description', 'published', 'profile']