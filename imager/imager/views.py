from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login


def home(request):
    return render(request, 'index.html')


def detail(request):
    return HttpResponse("You're looking at question")

def index(request):
    return render(request, 'index.html')


def test(request):
    return render(request, 'test.html')


