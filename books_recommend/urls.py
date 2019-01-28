"""books_recommend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', views.login),
    path('logout', views.logout),
    path('user/info', views.user_info),
    path('create_admin', views.create_admin),
    path('users', views.Users.as_view()),
    path('users/<int:id>', views.UsersDetail.as_view()),
    path('books', views.Books.as_view()),
    path('books/<int:id>', views.BooksDetail.as_view()),
    path('books/isbn/<isbn>', views.BooksIsbnDetail.as_view()),
    path('ratings/<int:id>', views.RatingsDetail.as_view()),
    path('ratings/user/<int:id>', views.RatingsUserDetail.as_view()),
    path('ratings/book/isbn/<isbn>', views.RatingsBookIsbnDetail.as_view()),
]
