from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from main.models import User


def insert(request):
    test1 = User(name='admin', password='password')
    test1.save()
    return HttpResponse('添加成功')
