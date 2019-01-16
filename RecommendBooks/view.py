from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    return HttpResponse('Hello World!')


def main(request):
    context = {'hello': 'Hello World'}
    return render(request, 'main.html', context)
