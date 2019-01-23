from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.forms.models import model_to_dict
import django.contrib.auth as auth
from main.models import Book
from main.one import RestJsonResponse
from django.core.exceptions import ObjectDoesNotExist
import json


def users_list(request):
    users = auth.models.User.objects.all()
    return RestJsonResponse(users)


def login(request):
    username = request.GET.get('username', 'dd')
    password = request.GET.get('password', 'ps')
    user = auth.authenticate(username=username, password=password)
    if user is None:
        return RestJsonResponse(msg='wrong username or password', code=403, status=403)
    auth.login(request, user)
    return RestJsonResponse({
        'username': username,
        'password': password,
    })


def logout(request):
    auth.logout(request)
    return RestJsonResponse()


def create_admin(request):
    user = auth.models.User.objects.create_superuser('admin', 'none', 'password')
    user.save()


def books_list(request):
    if request.method == 'GET':
        books = Book.objects.all()
        return RestJsonResponse(books)
    elif request.method == 'POST':
        book = Book(**request.info)
        book.id = None
        book.save()
        return RestJsonResponse()


def books_detail(request, id):
    if request.method == 'GET':
        book = Book.objects.get(id=id)
        return RestJsonResponse(book)
    elif request.method == 'PUT':
        book = Book.objects.filter(id=id)
        book.update(**request.info)
        return RestJsonResponse(Book.objects.get(id=id))
    elif request.method == 'DELETE':
        book = Book.objects.filter(id=id)
        book.delete()
        return RestJsonResponse()
