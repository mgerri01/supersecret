from __future__ import unicode_literals
import datetime
from django.db import models
from ..login.models import User
# Create your models here.

class PlanManager(models.Manager):
    def myAdventures(self, userid):
        user = User.objects.get(id=userid)
        my_list = Plan.objects.filter(adventurers=user)
        return my_list
    def otherAdventures(self, userid):
        # fetch all plans for which the user is NOT an adventurer
        user = User.objects.get(id=userid)
        other_list = Plan.objects.exclude(adventurers=user)
        return other_list
    def otherAdventurers(self, planid):
        thisplan = Plan.objects.get(id=planid)
        thiscreator = thisplan.creator
        adventurers_list = (
            User.objects.filter(adventures=thisplan).exclude(id=thiscreator.id)
        )
        return adventurers_list
    def validAdventure(self, formdata):
        errors = []
        # no empty entries
        if len(formdata['destination']) < 1:
            errors.append('Please include a destination.')
        if len(formdata['description']) < 1:
            errors.append('Please include a description.')
        if len(formdata['startdate']) < 1:
            errors.append('Please include a travel start date.')
        if len(formdata['enddate']) < 1:
            errors.append('Please include a travel end date.')

        print formdata['startdate']
        print formdata['enddate']
        try:
            startdate = datetime.datetime.strptime(
                formdata['startdate'], '%Y-%m-%d'
            )
            enddate = datetime.datetime.strptime(
                formdata['enddate'], '%Y-%m-%d'
            )
            print enddate
            print startdate
            if startdate < datetime.datetime.today():
                errors.append('Travel start date must be in the future.')
            if enddate < startdate:
                errors.append('Travel end date cannot be before start date.')
        except ValueError:
            errors.append('Invalid Format')
        return errors
    def createAdventure(self, formdata, userid):
        new_adventure = Plan.objects.create(
            destination=formdata['destination'],
            description=formdata['description'],
            startdate=formdata['startdate'],
            enddate=formdata['enddate'],
            creator=User.objects.get(id=userid)
        )
        new_adventure.adventurers.add(new_adventure.creator)
        return new_adventure
    def joinAdventure(self, planid, userid):
        this_adventure = Plan.objects.get(id=planid)
        this_user = User.objects.get(id=userid)
        if this_user in this_adventure.adventurers.all():
            return this_adventure
        else:
            this_adventure.adventurers.add(this_user)
            return this_adventure

class Plan(models.Model):
    destination = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    creator = models.ForeignKey(User, related_name='created')
    adventurers = models.ManyToManyField(User, related_name='adventures')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PlanManager()