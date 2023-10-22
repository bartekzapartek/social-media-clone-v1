from django.shortcuts import render, redirect

from .models import Post, Comment, UserProfile
from .forms import PostForm

from django.contrib.auth.decorators import login_required



@login_required(login_url = 'login')
def home_view(request):
    logged_user = UserProfile.objects.get(user = request.user)
    following_users = logged_user.following.all()
    following_posts = []

    for user in following_users:
        following_posts += Post.objects.filter(owner = user) 

    print(following_posts)
    
    context = {'following_posts' : following_posts} 
    return render(request, 'base/home.html', context)


def explore_view(request):
    posts = Post.objects.all()


    context = {}
    return render(request, 'base/home.html', context)

def post_view(request, pk):
    
    context = {}
    return render(request, 'base/post.html', context)


def user_profile_view(request, username):

    context = {}
    return render(request, 'base/home.html', context)


@login_required(login_url = 'login')
def create_view(request):
    post_form = PostForm()

    if request.method == 'POST':
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            post = post_form.save(commit = False)
            
            post.owner = request.user

            post.save()

            return redirect('home')


    context = {'post_form' : post_form}
    return render(request, 'base/create.html', context)