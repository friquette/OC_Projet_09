from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.messages import messages
from django.db import IntegrityError

from .models import Ticket, Review
from ..follows.models import UserFollows

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
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["image"]
        current_user = request.user

        try:
            ticket = Ticket.objects.create(title=title, description=description, image=image, user=current_user)
            ticket.save()
        except IntegrityError:
            messages.info(request, 'Vous avez oublié un champ.')

        return redirect('flux')
   
    return render(request, 'ticket.html')

def review(request):
    if request.method == "POST":
        current_user = request.user

        ticket_title = request.POST["title"]
        ticket_description = request.POST["description"]
        ticket_image = request.POST["image"]

        review_title = request.POST["headline"]
        review_content = request.POST["body"]
        rating = request.POST["rating"]

        ticket_for_review = Ticket.objects.create(title=ticket_title, 
            description=ticket_description,
            image=ticket_image,
            user=current_user
            )
        review = Review.objects.create(headline=review_title,
            body=review_content,
            rating=rating,
            ticket=ticket_for_review,
            user=current_user,
            )

        return redirect('flux')

    return render(request, 'review.html')


def update(request):
    if request.method == "POST":
        ticket_id = request.POST.get("id")
        current_ticket = Ticket.objects.get(pk=ticket_id)

        return redirect('flux')

    return render(request, 'flux.html')


