from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.forms.models import model_to_dict
import django.contrib.auth as auth
from django.views.decorators.http import require_http_methods
from django.views.generic.base import View

from main.models import Book, User, Rating
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


class Books(View):
    @staticmethod
    def get(request):
        page_number = int(request.GET.get('page_number', '1'))
        order_by = request.GET.get('order_by', 'id')
        books = Book.objects.order_by(order_by)
        if 'title' in request.GET:
            books = books.filter(title__contains=request.GET['title'])
        if 'isbn' in request.GET:
            books = books.filter(isbn__contains=request.GET['isbn'])
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


class BooksIsbnDetail(View):
    @staticmethod
    def get(request, isbn):
        book = Book.objects.get(isbn=isbn)
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


class Users(View):
    @staticmethod
    def get(request):
        page_number = int(request.GET.get('page_number', '1'))
        order_by = request.GET.get('order_by', 'id')
        users = User.objects.order_by(order_by)
        if 'name' in request.GET:
            users = users.filter(name__contains=request.GET['name'])
        if 'location' in request.GET:
            users = users.filter(location__contains=request.GET['location'])
        page_size = int(request.GET.get('page_size', str(users.count())))
        page = Paginator(users, page_size if page_size > 0 else 1).page(page_number)
        return RestJsonResponse(page)

    @staticmethod
    def post(request):
        user = User(**request.info)
        user.id = None
        user.save()
        return RestJsonResponse(user)


class UsersDetail(View):
    @staticmethod
    def get(request, id):
        user = User.objects.get(id=id)
        return RestJsonResponse(user)

    @staticmethod
    def put(request, id):
        user = User.objects.filter(id=id)
        request.info.pop('id')
        user.update(**request.info)
        return RestJsonResponse(User.objects.get(id=id))

    @staticmethod
    def delete(request, id):
        user = User.objects.filter(id=id)
        user.delete()
        return RestJsonResponse()


class RatingsDetail(View):
    @staticmethod
    def get(request, id):
        rating = Rating.objects.get(id=id)
        return RestJsonResponse(rating)

    @staticmethod
    def put(request, id):
        user = User.objects.filter(id=id)
        request.info.pop('id')
        user.update(**request.info)
        return RestJsonResponse(User.objects.get(id=id))

    @staticmethod
    def delete(request, id):
        user = User.objects.filter(id=id)
        user.delete()
        return RestJsonResponse()


class RatingsUserDetail(View):
    @staticmethod
    def get(request, id):
        page_number = int(request.GET.get('page_number', '1'))
        order_by = request.GET.get('order_by', 'id')
        ratings = Rating.objects.filter(user_id=id).order_by(order_by)
        page_size = int(request.GET.get('page_size', str(ratings.count())))
        page = Paginator(ratings, page_size if page_size > 0 else 1).page(page_number)
        return RestJsonResponse({
            'count': page.paginator.count,
            'content': list(map(lambda e: e.to_dict_with_book(), list(page))),
        })


class RatingsBookIsbnDetail(View):
    @staticmethod
    def get(request, isbn):
        page_number = int(request.GET.get('page_number', '1'))
        order_by = request.GET.get('order_by', 'isbn')
        ratings = Rating.objects.filter(isbn=isbn).order_by(order_by)
        page_size = int(request.GET.get('page_size', str(ratings.count())))
        page = Paginator(ratings, page_size if page_size > 0 else 1).page(page_number)
        return RestJsonResponse({
            'count': page.paginator.count,
            'content': list(map(lambda e: e.to_dict_with_user(), list(page))),
        })
