from django.shortcuts import render, redirect

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from base.models import UserProfile
from .forms import UserRegisterForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



def login_view(request):
    login_page = True

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if len(username) > 20:
            return redirect('login')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        
        return redirect('login')


    context = {'login_page' : login_page}
    return render(request, 'authen/authenticate.html', context)


def register_view(request):
    user_creation_form = UserRegisterForm()
    login_page = False

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')

        user_creation_form = UserCreationForm(request.POST)

        username_taken = True if User.objects.filter(username = username).count() == 1 else False

        if username_taken:
            return redirect('register')
        
        if user_creation_form.is_valid():
            user = user_creation_form.save()
            user_profile = UserProfile.objects.create(user = user)


            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                print('-' * 1000)

        return redirect('home')
        
    context = {'user_creation_form' : user_creation_form, 'login_page' : login_page}
    return render(request, 'authen/authenticate.html', context)


@login_required(login_url = 'login')
def logout_view(request):
    logout(request)

    context = {}
    return redirect('login')