from django.urls import path
from . import views

urlpatterns = [
    path('', views.flux, name='flux'),
    path('ticket', views.ticket, name="ticket"),
    path('review', views.review, name="review")
]
