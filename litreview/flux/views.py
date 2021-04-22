from django.shortcuts import render


def flux(request):
    return render(request, 'flux.html')
