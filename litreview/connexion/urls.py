from django.urls import path
from . import views

urlpatterns = [
    path('', views.log_in, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.log_out, name='logout'),
    path('succeedded', views.succeeded, name='succeeded'),
]
