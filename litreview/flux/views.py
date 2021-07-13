from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError

from .models import Ticket, Review
from .forms import TicketForm, ReviewForm
from follows.models import UserFollows

def flux(request):
    page = 'flux'
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

    for item in ticket:
        print(f'IMAGE URL: {item.image}')

    context = {
        'ticket': ticket,
        'review': review,
        'users': users,
        'items': items,
        'page': page,
    }

    return render(request, 'flux.html', context=context)


def posts(request):
    page = 'posts'
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
        'page': page,
    }

    return render(request, 'posts.html', context)

def ticket(request):
    if request.method == "POST":
        current_user = request.user
        ticket_form = TicketForm(request.POST, request.FILES)

        if ticket_form.is_valid():
            ticket = Ticket(
                title=request.POST['title'],
                description=request.POST['description'],
                image=request.FILES['image'],
                user=current_user,
            )
            ticket.save()

            return redirect('flux')
    else:
        ticket_form = TicketForm()
   
    context = {
        'ticket_form': ticket_form,
    }
    return render(request, 'ticket.html', context)

def review(request):
    page = 'flux'
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
        'page': page,
    }

    return render(request, 'review.html', context)


def response_to_ticket(request):
    page = 'flux'
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
        'review_form': review_form,
        'page': page,
    }
    return render(request, 'response.html', context)


def update_review(request):
    page = 'posts'
    type_to_modify = request.GET.get('type')
    item_id = request.GET.get('id')
    review_form = None

    if type_to_modify == 'ticket':
        if request.method == "POST":
            ticket_form = TicketForm(request.POST)

            if ticket_form.is_valid():
                if request.POST.get('update') == "Update":
                    current_ticket = ticket_forms(request, item_id)
                    current_ticket.save()

            return redirect("posts")

        else:
            current_ticket = Ticket.objects.get(pk=item_id)
            ticket_form = TicketForm(
                initial = {
                    'title': current_ticket.title,
                    'description': current_ticket.description,
                    'image': current_ticket.image,
                }
            )

    else:
        if request.method == "POST":
            ticket_form = TicketForm(request.POST)
            review_form = ReviewForm(request.POST)

            if ticket_form.is_valid() and review_form.is_valid():
                if request.POST.get('update') == "Update":
                    current_ticket = ticket_forms(request, Review.objects.get(pk=item_id).ticket.id)
                    current_review = review_forms(request, item_id)

                    current_review.save()
            return redirect("posts")
        else:
            current_review = Review.objects.get(pk=item_id)
            current_ticket = Ticket.objects.get(pk=current_review.ticket.id)
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
        'current_ticket': current_ticket,
        'review_form': review_form,
        'type': type_to_modify,
        'page': page,
    }

    return render(request, 'update.html', context)


def ticket_forms(request, item_id):
    current_ticket = Ticket.objects.get(pk=item_id)

    current_ticket.title = request.POST.get('title')
    current_ticket.description = request.POST.get('description')
    current_ticket.image = request.POST.get('image')

    return current_ticket


def review_forms(request, item_id):
    current_review = Review.objects.get(pk=item_id)

    current_review.headline = request.POST.get('headline')
    current_review.body = request.POST.get('body')
    current_review.rating = request.POST.get('rating')

    return current_review


def delete(request):
    id_to_delete = request.GET.get('id')
    type_to_delete = request.GET.get('type')

    if type_to_delete == "ticket":
        item_to_delete = Ticket.objects.get(pk=id_to_delete)
        if item_to_delete.review_set:
            item_to_delete.review_set.all().delete()
        item_to_delete.delete()

        return redirect("posts")

    elif type_to_delete == "review":
        item_to_delete = Review.objects.get(pk=id_to_delete)
        attached_ticket = Ticket.objects.get(pk=item_to_delete.ticket.id)
        
        item_to_delete.delete()
        attached_ticket.delete()

        return redirect("posts")
