from django.http import HttpResponse
from django.shortcuts import render


def detail(request):
    return HttpResponse("You're looking at question")


def test(request):
    return render(request, 'test.html')

from django.contrib.auth import authenticate, login

# def my_view(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         if user.is_active:
#             login(request, user)
#             # Redirect to a success page.
#         else:
#             pass
#             # Return a 'disabled account' error message
#     else:
#         pass
#         # Return an 'invalid login' error message.