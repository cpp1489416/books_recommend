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
    path('admin', admin.site.urls),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('user', views.User1.as_view()),
    path('ratings', views.ratings),
    path('recommendations', views.recommendations),
    path('create_admin', views.create_admin),
    path('books', views.Books.as_view()),
    path('books/<int:id>', views.BooksDetail.as_view()),
    path('books/<int:id>/rating', views.BooksDetailRating.as_view()),
    path('books/<int:id>/ratings', views.books_detail_ratings),
    path('users', views.Users.as_view()),
    path('users/<int:id>', views.UsersDetail.as_view()),
    path('users/<int:id>/ratings', views.users_detail_ratings),
    path('users/<int:id>/recommendations', views.users_detail_recommendations),
    path('ratings/<int:id>', views.RatingsDetail.as_view()),
    path('recommendations/update_similarity', views.recommendations_update_similarity),
    path('recommendations/regenerate_similarity', views.recommendations_regenerate_similarity),
    path('recommendations/precision', views.RecommendationsPrecision.as_view()),
    path('recommendations/recall', views.RecommendationsRecall.as_view()),
    path('recommendations/coverage', views.RecommendationsCoverage.as_view()),
    path('recommendations/f_measure', views.recommendations_f_measure),
    path('recommendations/status', views.recommendations_status),
    path('prometheus/metrics', views.PrometheusMetrics.as_view()),
]
