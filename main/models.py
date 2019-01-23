from django.db import models


# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    role = models.IntegerField(default=0)

class Book(models.Model):
    name = models.CharField(max_length=300)
    desc = models.CharField(max_length=300)
