from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.forms.models import model_to_dict
import django.contrib.auth as auth
from django.views.decorators.http import require_http_methods
from django.views.generic.base import View

from main.models import Book, User, Rating, Metrics
from main.one import RestJsonResponse
from django.core.exceptions import ObjectDoesNotExist
import json
import redis
import pickle
import logging
import operator
import math
import time
import sys
from . import recommendation
import prometheus_client

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


@require_http_methods(['POST'])
def register(request):
    return User1.post(request)


def logout(request):
    auth.logout(request)
    return RestJsonResponse()


class User1(View):
    @staticmethod
    def get(request):
        user = auth.get_user(request)
        # time.sleep(2)
        return RestJsonResponse(user)

    @staticmethod
    def put(request):
        user_id = auth.get_user(request).id
        print(user_id)
        return UsersDetail.put(request, user_id)

    @staticmethod
    def post(request):
        User.objects.create_user(
            username=request.info['username'],
            password=request.info['password'],
            email='')
        return RestJsonResponse(None)


def create_admin(request):
    user = auth.models.User.objects.create_superuser('admin', 'none', 'password')
    user.save()


def recommendations(request):
    user = auth.get_user(request)
    return users_detail_recommendations(request, user.id)


def ratings(request):
    user_id = auth.get_user(request).id
    return users_detail_ratings(request, user_id)


class Books(View):
    @staticmethod
    def get(request):
        page_number = int(request.GET.get('page_number', '1'))
        order_by = request.GET.get('order_by', 'id')
        books = Book.objects.filter(deleted=False).order_by(order_by)
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
        book = Book.objects.get(id=id)
        book.deleted = True
        book.save()
        Rating.objects.filter(book_id=book.id).update(deleted=True)
        time.sleep(1)
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


def books_detail_ratings(request, id):
    page_number = int(request.GET.get('page_number', '1'))
    order_by = request.GET.get('order_by', 'id')
    if 'user' not in order_by and 'rating' not in order_by:
        desc = False
        if order_by[0] == '-':
            desc = True
            order_by = order_by[1:]
        order_by = 'user__' + order_by
        if desc:
            order_by = '-' + order_by

    ratings = Rating.objects.filter(book__id=id, deleted=False).order_by(order_by)
    if 'user_name' in request.GET:
        ratings = ratings.filter(user__name__contains=request.GET['user_name'])

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
        request.info.pop('password')
        info = dict()
        info['username'] = request.info['username']
        info['email'] = request.info['email']
        info['location'] = request.info['location']
        info['age'] = request.info['age']
        info['avatar_url'] = request.info['avatar_url']
        user.update(**info)
        return RestJsonResponse(User.objects.get(id=id))

    @staticmethod
    def delete(request, id):
        user = User.objects.filter(id=id)
        user.delete()
        return RestJsonResponse()


def users_detail_ratings(request, id):
    page_number = int(request.GET.get('page_number', '1'))
    order_by = request.GET.get('order_by', 'id')
    if 'book' not in order_by and 'rating' not in order_by:
        desc = False
        if order_by[0] == '-':
            desc = True
            order_by = order_by[1:]
        order_by = 'book__' + order_by
        if desc:
            order_by = '-' + order_by

    ratings = Rating.objects.filter(user_id=id, deleted=False).order_by(order_by)
    page_size = int(request.GET.get('page_size', str(ratings.count())))
    page = Paginator(ratings, page_size if page_size > 0 else 1).page(page_number)
    return RestJsonResponse({
        'count': page.paginator.count,
        'content': list(map(lambda e: e.to_dict(), list(page))),
    })


def users_detail_recommendations(request, id):
    page_number = int(request.GET.get('page_number', '1'))
    page_size = int(request.GET.get('page_size', 100))
    k = int(request.GET.get('k', 5))
    ignore_rated = request.GET.get('ignore_rated', 'False').lower() == 'true'
    print(ignore_rated)
    book_ids_rated = set()

    if ignore_rated:
        books = Rating.objects.filter(user_id=id, deleted=False).values_list('book_id')
        for book in books:
            book_ids_rated.add(book[0])

    ratings = Rating.objects.filter(user_id=id, rating__gt=3)
    ranks = {}
    for item in ratings:
        if item.book_id not in recommendation.get_similarity_sorted():
            continue

        for book_id, p in recommendation.get_similarity_sorted()[item.book_id][0:k]:
            if book_id in book_ids_rated:
                continue
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


def recommendations_update_similarity(request):
    recommendation.update_similarity()
    return RestJsonResponse({
        'cost_seconds': recommendation.get_cost_seconds()
    })


def recommendations_regenerate_similarity(request):
    recommendation.regenerate_similarity()
    return RestJsonResponse({
        'cost_seconds': str(recommendation.get_cost_seconds()),
        'size': sys.getsizeof(recommendation.get_similarity()),
    })


def prometheus_metrics(request):
    return HttpResponse("fdsjfaoisdfjosjdifods")


class RecommendationsPrecision(View):
    @staticmethod
    def get(request):
        precisions = Metrics.objects.filter(algorithm_name='item_cf', type='precision').order_by('k')
        ans = []

        for precision in precisions:
            ans.append({
                'k': precision.k,
                'value': precision.value,
            })
        return RestJsonResponse(ans)

    @staticmethod
    def put(request):
        ks = request.info['ks']
        recommendation.get_redis_server().set('books_recommend:precision_mark', '')
        precisions = dict()
        for k in ks:
            precisions[k] = _recommendations_update_precision(k)

        Metrics.objects.filter(algorithm_name='item_cf', type='precision').delete()
        for k, value in precisions.items():
            precision = Metrics(algorithm_name='item_cf', type='precision', k=k, value=value, description='none')
            precision.save()

        recommendation.get_redis_server().delete('books_recommend:precision_mark')
        return RestJsonResponse(None)


class RecommendationsRecall(View):
    @staticmethod
    def get(request):
        recalls = Metrics.objects.filter(algorithm_name='item_cf', type='recall').order_by('k')
        ans = []
        for recall in recalls:
            ans.append({
                'k': recall.k,
                'value': recall.value,
            })
        return RestJsonResponse(ans)

    @staticmethod
    def put(request):
        ks = request.info['ks']
        recommendation.get_redis_server().set('books_recommend:recall_mark', '')
        precisions = dict()
        for k in ks:
            precisions[k] = _recommendations_update_recall(k)

        Metrics.objects.filter(algorithm_name='item_cf', type='recall').delete()
        for k, value in precisions.items():
            precision = Metrics(algorithm_name='item_cf', type='recall', k=k, value=value, description='none')
            precision.save()

        recommendation.get_redis_server().delete('books_recommend:recall_mark')
        return RestJsonResponse(None)


class RecommendationsCoverage(View):
    @staticmethod
    def get(request):
        coverages = Metrics.objects.filter(algorithm_name='item_cf', type='coverage').order_by('k')
        ans = []
        for coverage in coverages:
            ans.append({
                'k': coverage.k,
                'value': coverage.value,
            })
        return RestJsonResponse(ans)
        pass

    @staticmethod
    def put(request):
        ks = request.info['ks']
        recommendation.get_redis_server().set('books_recommend:coverage_mark', '')
        precisions = dict()
        for k in ks:
            precisions[k] = _recommendations_update_coverage(k)

        Metrics.objects.filter(algorithm_name='item_cf', type='coverage').delete()
        for k, value in precisions.items():
            precision = Metrics(algorithm_name='item_cf', type='coverage', k=k, value=value, description='none')
            precision.save()

        recommendation.get_redis_server().delete('books_recommend:coverage_mark')
        return RestJsonResponse(None)


def recommendations_f_measure(request):
    recalls = Metrics.objects.filter(algorithm_name='item_cf', type='recall').order_by('k')
    precisions = Metrics.objects.filter(algorithm_name='item_cf', type='precision').order_by('k')
    recall_dict = {}
    for recall in recalls:
        recall_dict[recall.k] = recall.value
    precision_dict = {}
    for precision in precisions:
        precision_dict[precision.k] = precision.value
    ans = []
    for k, recall in recall_dict.items():
        if k not in precision_dict:
            continue
        precision = precision_dict[k]
        ans.append({
            'k': k,
            'value': 2 * precision * recall / (precision + recall)
        })
    return RestJsonResponse(ans)


def recommendations_status(request):
    return RestJsonResponse({
        'precision_generating': recommendation.get_redis_server().get('books_recommend:precision_mark') is not None,
        'recall_generating': recommendation.get_redis_server().get('books_recommend:recall_mark') is not None,
        'coverage_generating': recommendation.get_redis_server().get('books_recommend:coverage_mark') is not None,
        'cost_seconds': recommendation.get_cost_seconds()
    })


def _recommendations_update_precision(k):
    hit_count = 0
    all_count = 0
    users = User.objects.filter()
    users_ids = set()
    for user in users:
        user_id = user.id
        users_ids.add(user.id)
        like_result = Rating.objects.filter(user_id=user_id, rating__gt=3, deleted=False).values_list('book_id')
        recommend_list = _get_recommendations_book_ids(user_id, k)
        for result in like_result:
            book_id = result[0]
            if book_id in recommend_list:
                hit_count += 1
        all_count += like_result.count()

    return hit_count / (all_count * 1.0)


def _recommendations_update_recall(k):
    hit_count = 0
    all_count = 0
    users = User.objects.filter()
    users_ids = set()
    for user in users:
        user_id = user.id
        users_ids.add(user.id)
        like_result = Rating.objects.filter(user_id=user_id, rating__gt=3, deleted=False).values_list('book_id')
        recommend_list = _get_recommendations_book_ids(user_id, k)
        for result in like_result:
            book_id = result[0]
            if book_id in recommend_list:
                hit_count += 1
        all_count += len(recommend_list)
    return hit_count / (all_count * 1.0)


def _recommendations_update_coverage(k):
    users = User.objects.filter()
    users_ids = []
    books = Book.objects.filter(deleted=False).values_list('id')
    books_ids = set()
    hit_books_ids = set()
    for user in users:
        user_id = user.id
        users_ids.append(user.id)
        like_result = Rating.objects.filter(user_id=user_id, rating__gt=3, deleted=False).values_list('book_id')
        for result in like_result:
            books_ids.add(result[0])
        recommend_list = _get_recommendations_book_ids(user_id, k)
        for book_id in recommend_list:
            hit_books_ids.add(book_id)
    return len(hit_books_ids) / (len(books_ids) * 1.0)


def _get_recommendations_book_ids(user_id, k):
    ratings = Rating.objects.filter(user_id=user_id, rating__gt=3, deleted=False)
    book_ids = set()
    for item in ratings:
        if item.book_id not in recommendation.get_similarity_sorted():
            continue
        for book_id, p in recommendation.get_similarity_sorted()[item.book_id][0:k]:
            book_ids.add(book_id)
    return book_ids



