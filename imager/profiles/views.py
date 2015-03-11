from django.shortcuts import render
from models import ImagerProfile

def profile_home(request):
    return render(request, 'profiles/profile_page.html', {'profile': ImagerProfile.objects.all()[0]})
# Create your views here.
