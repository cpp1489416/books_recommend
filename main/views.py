from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.forms.models import model_to_dict
import django.contrib.auth as auth
from django.views.decorators.http import require_http_methods
from django.views.generic.base import View

from main.models import Book
from main.one import RestJsonResponse
from django.core.exceptions import ObjectDoesNotExist
import json


def users_list(request):
    users = auth.models.User.objects.all()
    return RestJsonResponse(users)


@require_http_methods(['POST'])
def login(request):
    username = request.info['username']
    password = request.info['password']
    user = auth.authenticate(username=username, password=password)
    if user is None:
        return RestJsonResponse(msg='wrong username or password', code="403", status=200)
    auth.login(request, user)
    return RestJsonResponse()


def logout(request):
    auth.logout(request)
    return RestJsonResponse()


def user_info(request):
    user = auth.get_user(request)
    return RestJsonResponse(user)


def create_admin(request):
    user = auth.models.User.objects.create_superuser('admin', 'none', 'password')
    user.save()


class BooksAll(View):
    @staticmethod
    def get(request):
        page_number = int(request.GET.get('page_number', '1'))
        order_by = request.GET.get('order_by', 'id')
        books = Book.objects.order_by(order_by)
        if 'name' in request.GET:
            books = books.filter(name__contains=request.GET['name'])
        if 'desc' in request.GET:
            books = books.filter(desc__contains=request.GET['desc'])
        page_size = int(request.GET.get('page_size', str(books.count())))
        page = Paginator(books, page_size if page_size > 0 else 1).page(page_number)
        return RestJsonResponse(page)

    @staticmethod
    def post(request):
        book = Book(**request.info)
        book.id = None
        book.save()
        return RestJsonResponse(book)


class BooksDetail(View):
    @staticmethod
    def get(request, id):
        book = Book.objects.get(id=id)
        return RestJsonResponse(book)

    @staticmethod
    def put(request, id):
        book = Book.objects.filter(id=id)
        request.info.pop('id')
        book.update(**request.info)
        return RestJsonResponse(Book.objects.get(id=id))

    @staticmethod
    def delete(request, id):
        book = Book.objects.filter(id=id)
        book.delete()
        return RestJsonResponse()
