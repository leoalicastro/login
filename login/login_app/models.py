from django.db import models
import re
import bcrypt
from .models import *

class UserManager(models.Manager):
    def validator(self, post_data):
        errors = {}
        if len(post_data['fname']) < 2:
            errors['fname'] = "First name must be at least 2 characters"
        if len(post_data['lname']) < 2:
            errors['lname'] = "Last mame must be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "email format is invalid"
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be atleast 8 characters long"
        if post_data['password'] != post_data['confirm']:
            errors['confirm'] = "Passwords don't match"
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors['emailexist'] ="That email is already registered to another user"
        return errors
    def login_validator(self, post_data):
            errors = {}
            LoginUser = User.objects.filter(email=post_data['logemail'])
            if len(LoginUser) > 0:
                if bcrypt.checkpw(post_data['logpassword'].encode(), LoginUser[0].password.encode()):
                    print('password matches')
                else:
                    errors['logpassword'] = "The password is incorrect"
            else:
                errors['logemail'] = "That email does not exist"
            return errors


class User(models.Model):
    fname = models.CharField(max_length=255)
    lname= models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirm = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()