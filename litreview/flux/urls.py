from django.urls import path
from . import views

urlpatterns = [
    path('', views.flux, name='flux'),
    path('ticket', views.ticket, name="ticket"),
    path('review', views.review, name="review"),
    path('response', views.response_to_ticket, name="response"),
    path('update', views.update_review, name="update_review"),
    path('posts', views.posts, name="posts"),
    path('delete', views.delete, name="delete"),
]
