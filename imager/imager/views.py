from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from imager_images.models import Photo

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
