from django.core.exceptions import ObjectDoesNotExist
from django.db import models

# Create your models here.
from django.forms import model_to_dict


class User(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30,default='password')
    role = models.IntegerField(default=0)
    location = models.CharField(max_length=250, default='default')
    age = models.IntegerField(default=-1)

    def to_dict(self):
        return model_to_dict(self)


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='default')
    published_year = models.CharField(max_length=255, default='default')
    publisher = models.CharField(max_length=255, default='default')
    image_url = models.CharField(max_length=255, default='default')
    isbn = models.CharField(max_length=13, default='default')

    def to_dict(self):
        return model_to_dict(self)


class Rating(models.Model):
    user_id = models.IntegerField(default=0)
    isbn = models.CharField(max_length=13, default='default')
    rating = models.IntegerField(default=0, null=False)

    def to_dict(self):
        return model_to_dict(self)

    def to_dict_with_book(self):
        ans = model_to_dict(self)
        try:
            ans['book'] = Book.objects.get(isbn=ans['isbn']).to_dict()
        except ObjectDoesNotExist:
            ans['book'] = {
                'title': 'Does Not Exist'
            }
            pass
        return ans

    def to_dict_with_user(self):
        ans = self.to_dict()
        ans['user'] = User.objects.get(id=ans['user_id']).to_dict()
        return ans
