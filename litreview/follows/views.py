from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect

from .models import UserFollows


def follows(request):
    if "follow" in request.POST: 
        if request.method == 'POST':
            user_to_follow = request.POST.get('username', False)
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

    user_followed = UserFollows.objects.filter(user=request.user).order_by('followed_user__username')

    for follow in user_followed:
        print(follow.followed_user)
   
    context = {'follows': user_followed}

    return render(request, 'follows.html', context=context)


def unfollows(request):
    if 'unfollow_button' in request.POST:
        user_to_unfollow = request.POST.get('unfollow_button')
        unfollowed_user = UserFollows.objects.filter(followed_user__username=user_to_unfollow).delete()

        messages.info(request, f"L'utilisateur {user_to_unfollow} a bien été unfollow.")
            
        return redirect('follows')

def print_dict(context):
    print(context)
