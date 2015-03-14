from django.shortcuts import render, redirect
from imager_images.models import Photo, Album
from profiles.models import ImagerProfile
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from forms import PhotoForm, AlbumForm
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
    if not request.user.is_authenticated():
        return redirect('/accounts/login/')

    return render(request, 'profile.html', {'profile': ImagerProfile.objects.get(pk=request.user.id)})


class ProfileUpdate(UpdateView):
    model = ImagerProfile


class PhotoCreate(CreateView):
    model = Photo
    fields = ['title', 'description', 'photo', 'published']

    def form_valid(self, form):
        form.instance.profile = ImagerProfile.objects.get(pk=self.request.user.id)
        return super(PhotoCreate, self).form_valid(form)


class PhotoUpdate(UpdateView):
    model = Photo
    fields = ['title', 'description', 'published']


class PhotoDelete(DeleteView):
    model = Photo


class AlbumCreate(CreateView):
    model = Album
    form_class = AlbumForm

    def get_initial(self):
        initial = super(AlbumCreate, self).get_initial()
        initial['user'] = self.request.user
        return initial

    def form_valid(self, form):
        form.instance.profile = ImagerProfile.objects.get(pk=self.request.user.id)
        return super(AlbumCreate, self).form_valid(form)


class AlbumUpdate(UpdateView):
    model = Album
    form_class = AlbumForm

    def get_initial(self):
        initial = super(AlbumUpdate, self).get_initial()
        initial['user'] = self.request.user
        return initial


class AlbumDelete(DeleteView):
    model = Album

