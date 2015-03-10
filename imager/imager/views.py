from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login


def home(request):
    return render(request, 'index.html')



