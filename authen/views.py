from django.shortcuts import render, redirect

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from base.models import UserProfile
from .forms import UserRegisterForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages as login_errors



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
        
        login_errors.error(request, "Username or password does not match. Try again")
        return redirect('login')


    context = {'login_page' : login_page, 'errors' : login_errors}
    return render(request, 'authen/authenticate.html', context)


def register_view(request):
    user_creation_form = UserRegisterForm()
    login_page = False

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')

        if confirm_password != password:
            login_errors.error(request, "Password confirmation does not match. Try again")
            return redirect('register')   

        user_creation_form = UserCreationForm(request.POST)

        username_taken = True if User.objects.filter(username = username).count() == 1 else False

        if username_taken:
            login_errors.error(request, "Username is taken. Try again")
            return redirect('register')
        
        if user_creation_form.is_valid():
            user = user_creation_form.save()
            user_profile = UserProfile.objects.create(user = user)


            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect('home')


        login_errors.error(request, "Password is not strong enough. Try again")
        return redirect('register')   
            
            
        
    context = {'user_creation_form' : user_creation_form, 'login_page' : login_page, 'errors' : login_errors}
    return render(request, 'authen/authenticate.html', context)


@login_required(login_url = 'login')
def logout_view(request):
    logout(request)

    context = {}
    return redirect('login')