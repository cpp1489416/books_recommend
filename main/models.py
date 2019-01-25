from django.db import models

# Create your models here.
from django.forms import model_to_dict


class User(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    role = models.IntegerField(default=0)

    def to_dict(self):
        return model_to_dict(self)


class Book(models.Model):
    name = models.CharField(max_length=300)
    desc = models.CharField(max_length=300)

    def to_dict(self):
        return model_to_dict(self)
