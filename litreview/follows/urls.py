from django.urls import path

from . import views

urlpatterns = [
    path('', views.follows, name='follows'),
    path('unfollow/', views.unfollows, name='unfollows')
]
