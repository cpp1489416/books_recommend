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
import redis
import pickle
import logging
import operator
import math
import time
from . import recommendation

logger = logging.getLogger(__name__)


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


def user(request):
    user = auth.get_user(request)
    # time.sleep(2)
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
        time.sleep(1)
        return RestJsonResponse(Book.objects.get(id=id))

    @staticmethod
    def delete(request, id):
        book = Book.objects.filter(id=id)
        book.delete()
        return RestJsonResponse()


class BooksDetailRating(View):
    @staticmethod
    def get(request, id):
        user_id = auth.get_user(request).id
        time.sleep(1)
        try:
            rating = Rating.objects.get(user_id=user_id, book_id=id)
            return RestJsonResponse(rating.to_dict_without_user_and_book())
        except Rating.DoesNotExist:
            return RestJsonResponse(code='404', msg='no such rating')

    @staticmethod
    def put(request, id):
        user_id = auth.get_user(request).id
        rating_id = None
        try:
            rating_id = Rating.objects.get(user_id=user_id, book_id=id).id
        except Rating.DoesNotExist:
            pass
        print(request.info)
        rating = Rating(book_id=id, user_id=user_id, rating=request.info['rating'])
        rating.id = rating_id
        rating.save()
        time.sleep(1)
        return RestJsonResponse()


class BooksDetailRatings(View):
    @staticmethod
    def get(request,id):
        page_number = int(request.GET.get('page_number', '1'))
        order_by = request.GET.get('order_by', 'id')
        ratings = Rating.objects.filter(book__id=id).order_by(order_by)
        if 'user_name' in request.GET:
            ratings = ratings.filter(user__username__contains=request.GET['user_name'])

        page_size = int(request.GET.get('page_size', str(ratings.count())))
        page = Paginator(ratings, page_size if page_size > 0 else 1).page(page_number)
        return RestJsonResponse({
            'count': page.paginator.count,
            'content': list(map(lambda e: e.to_dict(), list(page))),
        })


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
    def get(request, user_id):
        page_number = int(request.GET.get('page_number', '1'))
        order_by = request.GET.get('order_by', 'id')
        ratings = Rating.objects.filter(user_id=user_id).order_by(order_by)
        page_size = int(request.GET.get('page_size', str(ratings.count())))
        page = Paginator(ratings, page_size if page_size > 0 else 1).page(page_number)
        return RestJsonResponse({
            'count': page.paginator.count,
            'content': list(map(lambda e: e.to_dict_with_book(), list(page))),
        })



def recommendations(request):
    user = auth.get_user(request)
    return recommendations_user(request, user.id)


def recommendations_user(request, user_id):
    page_number = int(request.GET.get('page_number', '1'))
    page_size = int(request.GET.get('page_size', 100))
    k = int(request.GET.get('k', 5))

    ratings = Rating.objects.filter(user_id=user_id, rating__gt=3)
    ranks = {}
    for item in ratings:
        for book_id, p in recommendation.get_similarity_sorted()[item.book_id][0:k]:
            ranks.setdefault(book_id, 0.0)
            ranks[book_id] += p * 1

    ranks = sorted(ranks.items(), key=operator.itemgetter(1), reverse=True)

    books = []
    for rank in ranks[page_size * (page_number - 1): min(page_size * page_number, Book.objects.count())]:
        book = Book.objects.get(id=rank[0]).to_dict()
        book['rank'] = rank[1]
        books.append(book)

    return RestJsonResponse({
        'count': len(ranks),
        'content': books
    })


def recommendation_update_similarity(request):
    recommendation.update_similarity()
    return RestJsonResponse({
        'cost_seconds:': recommendation.get_cost_seconds()
    })
