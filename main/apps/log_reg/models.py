from __future__ import unicode_literals

from django.db import models

import re
import bcrypt

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
pass_regex = re.compile(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{8,}$')

class UserManager(models.Manager):
    
    def reg_validate(self, postData):   
        errors = []

        if len(postData['first'])< 2 or len(postData['last']) < 2:
            errors.append("First and Last names must be at least 2 characters")
        if not postData['first'].isalpha() or not postData['last'].isalpha():
            errors.append("First and Last names cannot include numbers or specail characters")
        if not email_regex.match(postData['email']):
            errors.append("Email address is not vaild")
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors.append("User already exists")
        if not pass_regex.match(postData['pw']):
            errors.append("Password is not vaild")
        if not postData['pw'] == postData['pw_confirm']:
            errors.append("Passwords must match")
       
        if not errors:
            hashed = bcrypt.hashpw((postData['pw'].encode()), bcrypt.gensalt(5))

            user = User(first_name=postData['first'], last_name=postData['last'], email=postData['email'], password=hashed)
            user.save()
            return user
        else:
            return errors

    def log_validate(self, postData):
        errors = []

        if len(self.filter(email=postData['email'])) > 0:
            user = self.filter(email=postData['email'])[0]
            if not bcrypt.checkpw(postData['pw'].encode(), user.password.encode()):
                errors.append("Incorrect password")
        else:
            errors.append("User does not exist. Please register.")
        
        if errors:
            return errors
        else:
            return user

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length = 255, null=True)
    ceated_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()
    def __str__(self):
        return self.email