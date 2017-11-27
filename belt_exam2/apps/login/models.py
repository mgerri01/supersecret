# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
from django.db import models

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
    def validate_login(self, formdata):
        errors = []
        if len(self.filter(username=formdata['username'])) > 0:
            user = self.filter(username=formdata['username'])[0]
            if not bcrypt.checkpw(formdata['password'].encode(), user.password.encode()):
                errors.append('Incorrect Password')
        else:
            errors.append('Username is not registered')

        if errors:
            return errors

        return user

    def validate_registration(self, formdata):
        errors = []
        if len(formdata['first_name']) < 2 or len(formdata['last_name']) < 2:
            errors.append("name fields must be at least 3 characters")
        if len(formdata['password']) < 8:
            errors.append("password must be at least 8 characters")

        if not re.match(NAME_REGEX, formdata['first_name']) or not re.match(NAME_REGEX, formdata['last_name']):
            errors.append('name fields must be letter characters only')
        if len(User.objects.filter(username=formdata['username'])) > 0:
            errors.append("Username already in use")
        if formdata['password'] != formdata['password_confirm']:
            errors.append("passwords do not match")
        if not errors:
            hashed = bcrypt.hashpw((formdata['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                first_name=formdata['first_name'],
                last_name=formdata['last_name'],
                username=formdata['username'],
                password=hashed
            )
            return new_user
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=255)
    objects = UserManager()
    def __str__(self):
        return self.username