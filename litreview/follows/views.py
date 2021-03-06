from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect

from .models import UserFollows


@login_required
def follows(request):
    page = 'follow'
    current_user = request.user

    if "follow" in request.POST:
        if request.method == 'POST':
            user_to_follow = request.POST.get('username', False)

            if User.objects.filter(username=user_to_follow).exists():
                followed_user = User.objects.get(username=user_to_follow)
                if followed_user == current_user:
                    messages.info(
                        request,
                        "Vous ne pouvez pas vous suivre vous-même."
                    )
                else:
                    try:
                        follow = UserFollows.objects.create(
                            user=current_user,
                            followed_user=followed_user
                        )
                        follow.save()
                    except IntegrityError:
                        messages.info(
                            request,
                            'Vous ne pouvez pas suivre un utilisateur \
que vous suivez déjà.'
                        )
                return redirect('follows')
            else:
                messages.info(request, "L'utilisateur recherché n'existe pas.")
                return redirect('follows')

    user_followed = UserFollows.objects.filter(user=current_user).order_by(
        'followed_user__username'
    )
    followed_by = UserFollows.objects.filter(
        followed_user=current_user
    ).order_by('user__username')

    context = {
        'follows': user_followed,
        'followed_by': followed_by,
        'current_user': current_user,
        'page': page,
    }

    return render(request, 'follows.html', context=context)


def unfollows(request):
    current_user = request.user
    if 'unfollow_button' in request.POST:
        user_to_unfollow = request.POST.get('unfollow_button')
        unfollowed_user = UserFollows.objects.filter(user=current_user).get(
            followed_user__username=user_to_unfollow
        )

        unfollowed_user.delete()

        messages.info(
            request,
            f"L'utilisateur {user_to_unfollow} a bien été unfollow."
        )

        return redirect('follows')
