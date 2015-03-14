from django.shortcuts import render, redirect
from imager_images.models import Photo, Album
from profiles.models import ImagerProfile
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from forms import PhotoForm, AlbumForm, ProfileForm
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

    return render(request, 'profile.html',
                  {'profile': ImagerProfile.objects.get(pk=request.user.id)})


class ProfileUpdate(UpdateView):
    model = ImagerProfile
    form_class = ProfileForm

    def dispatch(self, request, *args, **kwargs):
        if int(self.kwargs['pk']) != self.request.user.id:
            return redirect('/accounts/login/')
        return super(ProfileUpdate, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(ProfileUpdate, self).get_initial()
        initial['user'] = self.request.user
        initial['profile'] = ImagerProfile.objects.get(user=self.request.user)


class PhotoCreate(CreateView):
    model = Photo
    fields = ['title', 'description', 'photo', 'published']

    def form_valid(self, form):
        form.instance.profile = ImagerProfile.objects.get(
            pk=self.request.user.id)
        return super(PhotoCreate, self).form_valid(form)


class PhotoUpdate(UpdateView):
    model = Photo
    fields = ['title', 'description', 'published']

    def dispatch(self, request, *args, **kwargs):
        photo_profile = Photo.objects.get(id=int(self.kwargs['pk'])).profile
        user_profile = ImagerProfile.objects.get(user=self.request.user)
        if photo_profile != user_profile:
            return redirect('/accounts/login/')
        return super(PhotoUpdate, self).dispatch(request, *args, **kwargs)


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
        form.instance.profile = ImagerProfile.objects.get(
            pk=self.request.user.id)
        return super(AlbumCreate, self).form_valid(form)


class AlbumUpdate(UpdateView):
    model = Album
    form_class = AlbumForm

    def get_initial(self):
        initial = super(AlbumUpdate, self).get_initial()
        initial['user'] = self.request.user
        return initial

    def dispatch(self, request, *args, **kwargs):
        album_profile = Album.objects.get(id=int(self.kwargs['pk'])).profile
        user_profile = ImagerProfile.objects.get(user=self.request.user)
        if album_profile != user_profile:
            return redirect('/accounts/login/')
        return super(AlbumUpdate, self).dispatch(request, *args, **kwargs)


class AlbumDelete(DeleteView):
    model = Album
