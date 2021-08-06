from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('flux')
        else:
            messages.info(request, 'Identifiant ou mot de passe incorrects.')
            return redirect('/')
    else:
        return render(request, 'login.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == "":
            messages.info(
                request,
                "Vous n'avez pas renseigné de mot de passe."
            )
            return redirect('register')
        elif password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Cet identifiant est déjà pris.')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password1
                )
                user.save()
                return redirect('succeeded')
        else:
            messages.info(request, 'Les mots de passe ne correspondent pas.')
            return redirect('register')

    else:
        return render(request, 'register.html')


def succeeded(request):
    return render(request, 'creation_succeeded.html')


def log_out(request):
    logout(request)
    return redirect('login')
