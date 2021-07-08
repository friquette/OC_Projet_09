from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError

from .models import Ticket, Review
from .forms import TicketForm, ReviewForm
from follows.models import UserFollows

def flux(request):
    current_user = request.user
    ticket = Ticket.objects.all()
    review = Review.objects.all()
    followed_users = UserFollows.objects.all()

    tick_and_rev = []
    users = [current_user,]

    for user in followed_users:
        users.append(user.followed_user)

    for tick in ticket:
        tick_and_rev.append(tick)

    for rev in review:
        tick_and_rev.append(rev)
    
    items = sorted(tick_and_rev, key=lambda item:item.time_created, reverse=True)

    context = {
        'ticket': ticket,
        'review': review,
        'users': users,
        'items': items,
    }

    return render(request, 'flux.html', context=context)


def posts(request):
    current_user = request.user
    ticket = Ticket.objects.filter(user=current_user)
    review = Review.objects.filter(user=current_user)
    followed_users = UserFollows.objects.all()

    tick_and_rev = []

    for tick in ticket:
        tick_and_rev.append(tick)

    for rev in review:
        tick_and_rev.append(rev)
    
    items = sorted(tick_and_rev, key=lambda item:item.time_created, reverse=True)

    if request.GET.get('delete'):
        return redirect('delete')

    context = {
        'ticket': ticket,
        'review': review,
        'items': items,
    }

    return render(request, 'posts.html', context)

def ticket(request):
    if request.method == "POST":
        current_user = request.user
        ticket_form = TicketForm(request.POST)

        if ticket_form.is_valid():
            ticket = Ticket(
                title=request.POST['title'],
                description=request.POST['description'],
                image=request.POST['image'],
                user=current_user
            )

            ticket.save()

            return redirect('flux')
    else:
        ticket_form = TicketForm()
   
    return render(request, 'ticket.html', {'ticket_form': ticket_form})

def review(request):
    if request.method == "POST":
        current_user = request.user
        ticket_form = TicketForm(request.POST)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            ticket = Ticket(
                title=request.POST['title'],
                description=request.POST['description'],
                image=request.POST['image'],
                user=current_user
            )
            review = Review(
                headline=request.POST["headline"],
                body=request.POST["body"],
                rating=request.POST["rating"],
                ticket=ticket,
                user=current_user
            )

            ticket.save()
            review.save()

            return redirect('flux')

    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }

    return render(request, 'review.html', context)


def response_to_ticket(request):
    ticket_id = request.GET.get("create_review")
    current_ticket = Ticket.objects.get(pk=ticket_id)

    if request.method == "POST":
        current_user = request.user
        ticket_form = TicketForm(request.POST)
        review_form = ReviewForm(request.POST)

        if review_form.is_valid() and ticket_form.is_valid():
            if request.POST.get('critique') == "Répondre à la demande":
                current_ticket.title=request.POST.get('title')
                current_ticket.description=request.POST.get('description')
                current_ticket.image=request.POST.get('image')
 
                review = Review(
                    headline=request.POST["headline"],
                    body=request.POST["body"],
                    rating=request.POST["rating"],
                    ticket=current_ticket,
                    user=current_user
                )

                review.save()

            return redirect('flux')

    else:
        ticket_form = TicketForm(
            initial = {
                'title': current_ticket.title,
                'description': current_ticket.description,
                'image': current_ticket.image,
            }
        )
        review_form = ReviewForm()

    context = {
        'ticket_form': ticket_form,
        'review_form': review_form
    }
    return render(request, 'response.html', context)


def update_review(request):
    ticket_id = request.GET.get("update")
    current_review = Review.objects.get(pk=ticket_id)
    current_ticket = Ticket.objects.get(pk=current_review.ticket.id)
    

    if request.method == "POST":
        current_user = request.user

        ticket_form = TicketForm(request.POST)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            if request.POST.get('critique') == "Publier une critique":
                current_ticket.title = request.POST.get('title')
                current_ticket.description = request.POST.get('description')
                current_ticket.image = request.POST.get('image')

                current_review.headline = request.POST.get('headline')
                current_review.body = request.POST.get('headline')
                current_review.rating = request.POST.get('headline')

                if current_ticket.user == current_user:
                    current_ticket.save()

                current_review.save()

        return redirect('flux')

    else:
        ticket_form = TicketForm(
            initial = {
                'title': current_ticket.title,
                'description': current_ticket.description,
                'image': current_ticket.image,
            }
        )
        review_form = ReviewForm(
            initial = {
                'headline': current_review.headline,
                'body': current_review.body,
                'rating': current_review.rating,
            }
        )

    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }

    return render(request, 'review.html', context)


def update_ticket(request):
    pass


def delete(request):
    pass