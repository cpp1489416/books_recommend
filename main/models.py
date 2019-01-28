from django.db import models

# Create your models here.
from django.forms import model_to_dict


class User(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    role = models.IntegerField(default=0)
    location = models.CharField(max_length=100, default='default')
    age = models.DecimalField(decimal_places=5, max_digits=40, default=-1)

    def to_dict(self):
        return model_to_dict(self)


class Book(models.Model):
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=500, default='default')
    published_year = models.CharField(max_length=100, default='default')
    publisher = models.CharField(max_length=300, default='default')
    image_url = models.CharField(max_length=500, default='default')
    isbn = models.CharField(max_length=100, default='default', unique=True)

    def to_dict(self):
        return model_to_dict(self)


class Rating(models.Model):
    user_id = models.IntegerField(default=0)
    isbn = models.CharField(max_length=400, default='default')
    rating = models.DecimalField(decimal_places=5, max_digits=40, default=-1)

    def to_dict(self):
        return model_to_dict(self)

    def to_dict_with_book(self):
        ans = model_to_dict(self)
        ans['book'] = Book.objects.get(isbn=ans['isbn']).to_dict()
        return ans

    def to_dict_with_user(self):
        ans = self.to_dict()
        ans['user'] = User.objects.get(id=ans['user_id']).to_dict()
        return ans
