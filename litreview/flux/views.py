from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .models import Ticket, Review


def flux(request):
    ticket = Ticket.objects.all()
    review = Review.objects.all()

    context = {
        'ticket': ticket,
        'review': review
    }
    return render(request, 'flux.html', context=context)

def ticket(request):
    title = None
    description = None


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
    
    #context = {"title": title, "description": description, "image": image}
   
    return render(request, 'ticket.html')

def review(request):
    return render(request, 'review.html')
