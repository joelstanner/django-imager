from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from imager_images.models import Photo

def home(request):
    return render(request, 'index.html', {'random_photo': Photo.random_image.all()[0]})
