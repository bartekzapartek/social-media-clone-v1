from django.shortcuts import render

from .models import Post, Comment, UserProfile
from django.contrib.auth.decorators import login_required



@login_required(login_url = 'login')
def home_view(request):
    #logged_user = UserProfile.objects.get(user = request.user)

    context = {}
    return render(request, 'base/home.html', context)


def explore_view(request):

    context = {}
    return render(request, 'base/home.html', context)

def post_view(request, pk):
    
    context = {}
    return render(request, 'base/post.html', context)


def user_profile_view(request, pk):

    context = {}
    return render(request, 'base/home.html', context)