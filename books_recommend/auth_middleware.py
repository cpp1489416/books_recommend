from django.utils.deprecation import MiddlewareMixin
from django.http.response import HttpResponse
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from main.one import RestJsonResponse
import json


class AuthMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        print(request.path)
        if 'application/json' in request.META['CONTENT_TYPE']:
            request.info = json.loads(request.body)
        if request.path == '/login' or request.path == '/create_admin':
            return
        if not request.user.is_authenticated:
            return JsonResponse(status=403, data={
                'code': 403,
                'msg': 'auth failure',
                'data': None,
            })

    @staticmethod
    def process_response(request, response):
        return response

    @staticmethod
    def process_exception(request, exception):
        if isinstance(exception, ObjectDoesNotExist):
            return RestJsonResponse(msg='not found', code='404')
