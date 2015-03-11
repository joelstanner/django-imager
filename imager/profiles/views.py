from django.shortcuts import render
from models import ImagerProfile
from django.views.generic.detail import DetailView

def profile_home(request):
    return render(request, 'profiles/profile_page.html', {'profile': ImagerProfile.objects.all()[0]})
# Create your views here.

class ProfileDetailView(DetailView):
    model = ImagerProfile

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        return context