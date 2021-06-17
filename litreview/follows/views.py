from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect

from .models import UserFollows


def follows(request):
    if request.method == 'POST':
        user_to_follow = request.POST['username']
        current_user = request.user

        if User.objects.filter(username=user_to_follow).exists():
            followed_user = User.objects.get(username=user_to_follow)
            if followed_user == current_user:
                messages.info(request, "Vous ne pouvez pas vous suivre vous-même.")
            else:
                try:
                    follow = UserFollows.objects.create(user=current_user, followed_user=followed_user)
                    follow.save()
                except IntegrityError:
                    messages.info(request, 'Vous ne pouvez pas suivre un utilisateur que vous suivez déjà.')
            return redirect('follows')
        else:
            messages.info(request, "L'utilisateur recherché n'existe pas.")
            return redirect('follows')

    user_followed = []
    for follow in UserFollows.objects.all().filter(user=request.user):
        user_followed.append(follow.followed_user.username)

    context = {'follows': user_followed}

    return render(request, 'follows.html', context=context)

def unfollows(request):
    if request.method == 'POST':
        user_to_unfollow = request.POST['username']
        current_user = request.user

        if User.objects.filter(username=user_to_unfollow).exists():
            unfollowed_user = User.objects.get(username=user_to_unfollow)
            
            try:
                unfollow = UserFollows.objects.delete(user=current_user, followed_user=unfollowed_user)
                unfollow.save()
            except IntegrityError:
                messages.info(request, "Vous ne pouvez supprimer un utilisateur qui n'est pas dans votre liste.")
                return redirect('follows')
        else:
            messages.info(request, "L'utilisateur recherché n'existe pas.")
            return redirect('follows')

    context = {'unfollows': user_to_unfollow}

    return render(request, 'unfollows.html', context)

def print_dict(context):
    print(context)
