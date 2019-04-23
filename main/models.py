from django.core.exceptions import ObjectDoesNotExist
from django.db import models

# Create your models here.
from django.forms import model_to_dict
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=100)
    role = models.IntegerField(default=0)
    location = models.CharField(max_length=250, default='default')
    age = models.IntegerField(default=-1)
    avatar_url = models.CharField(max_length=200)

    def to_dict(self):
        return model_to_dict(self)


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='default')
    published_year = models.CharField(max_length=255, default='default')
    publisher = models.CharField(max_length=255, default='default')
    image_url = models.CharField(max_length=255, default='default')
    isbn = models.CharField(max_length=13, default='default')
    deleted = models.BooleanField(default=False)

    def to_dict(self):
        return model_to_dict(self)


class Rating(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, null=False)
    deleted = models.BooleanField(default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book.id,
            'user_id': self.user.id,
            'rating': self.rating,
            'book': self.book.to_dict(),
            'user': self.user.to_dict()
        }

    def to_dict_without_user_and_book(self):
        return {
            'id': self.id,
            'book_id': self.book.id,
            'user_id': self.user.id,
            'rating': self.rating,
        }


class Metrics(models.Model):
    algorithm_name = models.CharField(max_length=100, default='default')
    type = models.CharField(max_length=100, default='default')
    k = models.IntegerField(default=0)
    value = models.FloatField()
    description = models.CharField(max_length=100, default='default')


