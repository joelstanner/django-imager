from django.shortcuts import render, redirect
from imager_images.models import Photo, Album
from profiles.models import ImagerProfile
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from forms import ProfileForm
from profiles.models import ImagerProfile


def profile(request):
    if not request.user.is_authenticated():
        return redirect('/accounts/login/')

    return render(request, 'profiles/profile.html',
                  {'profile': ImagerProfile.objects.get(pk=request.user.id)})


class ProfileUpdate(UpdateView):
    model = ImagerProfile
    form_class = ProfileForm

    def dispatch(self, request, *args, **kwargs):
        if int(self.kwargs['pk']) != self.request.user.id:
            return redirect('/accounts/login/')
        return super(ProfileUpdate, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {'first_name': self.request.user.first_name,
                'last_name': self.request.user.last_name,
                'email': self.request.user.email}