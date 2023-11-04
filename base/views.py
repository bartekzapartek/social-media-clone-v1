from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from .models import Post, Comment, UserProfile
from .forms import PostForm

from django.contrib.auth.decorators import login_required



@login_required(login_url = 'login')
def home_view(request):
    logged_user = UserProfile.objects.get(user = request.user)
    following_users = logged_user.following.all()
    following_posts = []
    post_comments = []

    for user in following_users:
        following_posts += Post.objects.filter(owner = user) 
        post_comments += following_posts[-1].comment_set.all()[:2]

    
    context = {'following_posts' : following_posts, 'comments' : post_comments} 
    return render(request, 'base/home.html', context)


def explore_view(request):
    posts = Post.objects.all().order_by('-created')


    context = {'posts' : posts}
    return render(request, 'base/explore.html', context)

def post_view(request, pk):
    post = Post.objects.get(id = pk)
    likes_count = post.likes.count()
    comments = post.comment_set.all().order_by('-created')

    if request.method == "POST" and request.user.is_authenticated:
        comment_body = request.POST.get('comment')
        comment_owner = request.user
        comment_post = post

        comment = Comment.objects.create(

            owner = comment_owner,
            body = comment_body,
            post = comment_post

        )

        comment.save()

        return redirect('post', pk)

    
    context = {'post' : post, 'likes_count' : likes_count, 'comments' : comments}   
    return render(request, 'base/post-view.html', context)

@login_required(login_url = 'login')
def user_profile_view(request, username):
    user = User.objects.get(username = username)
    user_profile = UserProfile.objects.get(user = user)

    following_count = user_profile.following.count()
    followers_count = user_profile.followers.count()

    posts = Post.objects.filter(owner = user)

    context = {

        'username' : username,
        'following_count' : following_count,
        'followers_count' : followers_count,
        'posts' : posts

    }

    return render(request, 'base/user-profile.html', context)


@login_required(login_url = 'login')
def create_view(request):
    post_form = PostForm()

    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
       
        if post_form.is_valid():
            post = post_form.save(commit = False)
            
            post.owner = request.user

            post.save()

            return redirect('home')


    context = {'post_form' : post_form}
    return render(request, 'base/create.html', context)