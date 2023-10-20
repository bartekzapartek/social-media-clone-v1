from django.shortcuts import render

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


def login_view(request):


    context = {}
    return render(request, 'authen/authenticate.html', context)


def register_view(request):
    
    context = {}
    return render(request, 'authen/authenticate.html', context)


@login_required(login_url = 'login')
def logout_view(request):

    context = {}
    return render(request, 'authen/authenticate.html', context)