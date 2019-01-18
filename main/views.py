from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from main.models import User
from django.forms.models import model_to_dict


def insert(request):
    test1 = User(name='admin', password='password')
    test1.save()
    return HttpResponse('添加成功')


def list_users(request):
    users = User.objects.all()
    user_json = []
    for user in users:
        user_json.append(model_to_dict(user, fields=['id', 'name']))
    return JsonResponse(
        {
            'code': 0,
            'msg': '',
            'data': user_json,
        }
    )
