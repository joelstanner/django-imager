from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from models import Photo, Album
from profiles.models import ImagerProfile
from forms import AlbumForm


@login_required
def library(request):

    return render(request,
                  'imager_images/library.html',
                  {'profile': ImagerProfile.objects.get(pk=request.user.id)})


@login_required
def stream(request):

    profile = ImagerProfile.objects.get(pk=request.user.id)
    following = profile.following()
    recent_pics = profile.show_all_photos().order_by('date_uploaded')
    following_pics = []
    for followed in following:
        following_pics.append(followed.show_photos().order_by('date_uploaded'))
    return render(request, 'imager_images/profilestream.html',
                           {'profile': profile,
                            'profile_pics': recent_pics,
                            'following_pics': following_pics
                            })


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
