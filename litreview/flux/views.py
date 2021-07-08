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

                current_ticket.save()
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

    print(f'CURRENT TICKET: {current_ticket.description}')
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form
    }
    return render(request, 'response.html', context)

def update(request):
    if request.method == "POST":
        ticket_id = request.POST.get("id")
        current_ticket = Ticket.objects.get(pk=ticket_id)
        current_user = request.user

        print(f"CURRENT TICKET = {current_ticket}")

        return redirect('flux')



