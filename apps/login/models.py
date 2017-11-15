from __future__ import unicode_literals
from django.db import models
import bcrypt, re
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def login(self, postData):

        are_errors = False
        messages = []

        try:
            found_user = User.objects.get(email=postData['email'])
        except:
            found_user = False

        if len(postData['email']) < 1:
            messages.append("Email cannot be blank!")
            are_errors = True
        elif not EMAIL_REGEX.match(postData['email']):
            messages.append("Please enter a valid email!")
            are_errors = True
        elif not found_user:
            messages.append("No user found with this email address. Please register new user.")
            are_errors = True

        if are_errors:
            return {'result':"are_errors", 'messages':messages}
        if len(postData['password']) < 8:
            messages.append("Password must be at least 8 characters")
            return {'result':"are_errors", 'messages':messages}

        hashed_password = bcrypt.hashpw(str(postData['password']), str(found_user.salt))
        # print hashed_password

        if found_user.password != hashed_password:
            messages.append("Incorrect password! Please try again")
            are_errors = True


        if are_errors:
            return {'result':"are_errors", 'messages':messages}
        else:
            messages.append('Successfully logged in!')
            return {'result':'success', 'messages':messages, 'user':found_user}

    def register(self, postData):
        failed_validation = False
        messages = []
        if len(postData['name']) < 2:
            messages.append("Name must be at least 2 characters!")
            failed_validation = True
        if len(postData['alias']) < 2:
            messages.append("Alias must be at least 2 characters!")
            failed_validation = True
        try:
            found_user = User.objects.get(email=postData['email'])
        except:
            found_user = False
        if len(postData['email']) < 1:
            messages.append("Email is required!")
            failed_validation = True
        elif not EMAIL_REGEX.match(postData['email']):
            messages.append("Please enter a valid email!")
            failed_validation = True
        elif found_user:
            messages.append("This email is unavailable!")
            failed_validation = True
        if len(postData['password']) < 8:
            messages.append("Password must be at least 8 characters!")
            failed_validation = True
        elif postData['confirm_password'] != postData['password']:
            messages.append("Password confirmation failed, please enter the same password to confirm")
            failed_validation = True

        if failed_validation:
            return {'result':"failed_validation", 'messages':messages}
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(str(postData['password']), str(salt))
        User.objects.create(name=postData['name'], alias=postData['alias'], email=postData['email'], password=hashed_password, salt=salt)
        user = User.objects.get(email=postData['email'])
        return {'result':"Successfully registered new user", 'messages':messages, 'user':user}

class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    salt = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()