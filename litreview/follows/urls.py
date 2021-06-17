from django.urls import path
from . import views

urlpatterns = [
    path('', views.follows, name='follows'),
    path('', views.unfollows, name='unfollows')
]
