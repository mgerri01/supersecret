from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from ..login.models import User
from .models import Plan

# Create your views here.
def index(request):
    context = {
        'user': User.objects.filter(id=request.session['id']),
        'mytrips': Plan.objects.myAdventures(request.session['id']),
        'othertrips': Plan.objects.otherAdventures(request.session['id']),
    }
    return render(request, 'beltExam/index.html',context)

def destination(request, id):
    print User.objects.get(id=request.session['id']).adventures
    print User.objects.get(id=request.session['id']).created
    try:
        this_plan = Plan.objects.get(id=id)
        context = {
            'plan': this_plan,
            'others': Plan.objects.otherAdventurers(id)
        }
        return render(request, 'beltExam/destination.html', context)
    except ObjectDoesNotExist:
        return redirect(reverse('travels:index'))

def addScreen(request):
    return render(request, 'beltExam/add.html')

def join(request, id):
    Plan.objects.joinAdventure(id, request.session['id'])
    return redirect(reverse('travels:index'))

def addTrip(request):
    if request.method == 'POST':
        errors = Plan.objects.validAdventure(request.POST)
        if errors:
            for each in errors:
                messages.error(request, each)
            return redirect(reverse('travels:addScreen'))
        else:
            Plan.objects.createAdventure(request.POST, request.session['id'])
            return redirect(reverse('travels:index'))
    return redirect(reverse('travels:addScreen'))