from __future__ import unicode_literals
from .models import User
from django.shortcuts import render, redirect,reverse
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'login/index.html')

def register(request):
    new_user = User.objects.validate_registration(request.POST)
    if type(new_user) == list:
        for err in new_user:
            messages.error(request, err)
        return redirect('/')
    messages.success(request, "Successfully registered!, Now Please Login")
    return redirect('/')

def login(request):
    user = User.objects.validate_login(request.POST)
    if type(user) == list:
        for err in user:
            messages.error(request, err)
        return redirect('/')
    request.session['id'] = user.id
    messages.success(request, "Successfully logged in!")
    return redirect(reverse("beltExam:index"))

def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')
    messages.success(request, 'You have been logged out.')
    return redirect('/')