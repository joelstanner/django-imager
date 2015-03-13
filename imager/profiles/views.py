from django.shortcuts import render
from models import ImagerProfile
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required


def profile_home(request):
    return render(request,
                  'profiles/profile_page.html',
                  {'profile': ImagerProfile.objects.all()[0]}
                  )


class ProfileDetailView(DetailView):
    model = ImagerProfile

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['user_pk'] = int(self.request.user.pk)
        context['profile_pk'] = int(context['object'].user.pk)
        return context
