from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from .models import Post, Comment, UserProfile, Chat, Message
from .forms import PostForm

from django.db.models import Q

from django.contrib.auth.decorators import login_required


def get_recent_activity_chats(request):
    if request.user.is_authenticated:
        return Chat.objects.filter(
            Q(participant_1 = request.user) | Q(participant_2 = request.user)
            )[:3]

    return None
   

@login_required(login_url = 'login')
def home_view(request):
    logged_user = UserProfile.objects.get(user = request.user)
    following_users = logged_user.following.all()
    following_posts = []
    

    for user in following_users:
        following_posts += Post.objects.filter(owner = user) 


    
    context = {'following_posts' : following_posts, 'recent_activity_chats' : get_recent_activity_chats(request)} 
    return render(request, 'base/home.html', context)


@login_required(login_url = 'login')
def search_view(request):
    search_query = request.GET.get('q') if request.GET.get('q') != None else ''
    search_result = None

    context = {}
   
    if search_query != '':
        if search_query[0] == '@':
            search_result = User.objects.filter(username__icontains = search_query[1:])
            context = {'search_result' : search_result, 'result_type' : 'users'}

        elif search_query[0] == '#':
            search_result = Post.objects.filter(description__icontains = search_query[1:])
            context = {'search_result' : search_result, 'result_type' : 'posts'}

        else:
            pass



    context['recent_activity_chats'] = get_recent_activity_chats(request)
    return render(request, 'base/search.html', context)

def explore_view(request):
    posts = Post.objects.all().order_by('-created')

    context = {'posts' : posts, 'recent_activity_chats' : get_recent_activity_chats(request)}
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

    
    context = {

        'post' : post,
        'likes_count' : likes_count,
        'comments' : comments,
        'recent_activity_chats' : get_recent_activity_chats(request) 

              }   
    
    return render(request, 'base/post-view.html', context)

@login_required(login_url = 'login')
def user_profile_view(request, username):
    user = User.objects.get(username = username)
    user_profile = UserProfile.objects.get(user = user)

    following_count = user_profile.following.count()
    followers_count = user_profile.followers.count()

    follow_status = 'cannot'

    if request.user == user:
        follow_status = 'cannot'

    elif request.user in user_profile.followers.all():
        follow_status = 'unfollow'

    else:
        follow_status = 'follow'

   

    posts = Post.objects.filter(owner = user)


    if request.method == "POST":
        logged_user_profile = UserProfile.objects.get(user = request.user)

        if follow_status == 'follow':
            user_profile.followers.add(request.user)
            logged_user_profile.following.add(user)
        
        elif follow_status == "unfollow":
            user_profile.followers.remove(request.user)
            logged_user_profile.following.remove(user)

        return redirect('user-profile', user.username)


    context = {

        'username' : username,
        'following_count' : following_count,
        'followers_count' : followers_count,
        'posts' : posts,
        'follow_status' : follow_status,
        'recent_activity_chats' : get_recent_activity_chats(request)

    }


    return render(request, 'base/user-profile.html', context)


@login_required(login_url = 'login')
def followers_view(request, username):
    user = User.objects.get(username = username)
    user_profile = UserProfile.objects.get(user = user)

    followers = user_profile.followers.all()


    context = {'users' : followers, 'recent_activity_chats' : get_recent_activity_chats(request)}

    return render(request, 'base/show-followers.html', context)


@login_required(login_url = 'login')
def following_view(request, username):
    user = User.objects.get(username = username)
    user_profile = UserProfile.objects.get(user = user)

    following = user_profile.following.all()


    context = {'users' : following, 'recent_activity_chats' : get_recent_activity_chats(request)}

    return render(request, 'base/show-followers.html', context)


@login_required(login_url = 'login')
def create_view(request):
    post_form = PostForm()

    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
       
        if post_form.is_valid():
            post = post_form.save(commit = False)
            
            post.owner = request.user

            post.save()

            return redirect('user-profile', post.owner.username)

    context = {'post_form' : post_form, 'recent_activity_chats' : get_recent_activity_chats(request)}
    return render(request, 'base/create.html', context)


@login_required(login_url = 'login')
def delete_post_view(request, pk):
    post = Post.objects.get(id = pk)

    if request.user != post.owner:
        return redirect('home')
    
    if request.method == "POST":
        post.delete()
        return redirect('user-profile', post.owner.username)

    context = {'recent_activity_chats' : get_recent_activity_chats(request)}
    return render(request, 'base/delete-post.html', context)


@login_required(login_url = 'login')
def create_chat_room_view(request):

    logged_user_profile = UserProfile.objects.get(user = request.user)
    logged_user_following = logged_user_profile.following.all()

    if request.method == 'POST':
        receiver_username = request.POST.get('username')
        receiver = None

        try:
            receiver = User.objects.get(username = receiver_username)

        except:
            receiver = None


        if receiver != None:

            was_already_created_chat = True

            try:
                chat_id = Chat.objects.get(

                    (Q(participant_1 = receiver) & Q(participant_2 = request.user)) |
                    (Q(participant_1 = request.user) & Q(participant_2 = receiver))
                    
                    ).id

            except:
                was_already_created_chat = False

        
            if was_already_created_chat == True:
                return redirect('chat-content', chat_id)

            chat_room = Chat.objects.create(

                participant_1 = request.user,
                participant_2 = receiver,

            )

            chat_room.save()

            return redirect('chat-content', chat_room.id)
        
        return redirect('create-chat')

    context = {'following' : logged_user_following, 'recent_activity_chats' : get_recent_activity_chats(request)}
    return render(request, 'base/create-chat.html', context)


@login_required(login_url = 'login')
def show_chats_view(request):
    user_chats = Chat.objects.filter(

        Q(participant_1 = request.user) |
        Q(participant_2 = request.user)

    )

    context = {'chats' : user_chats, 'recent_activity_chats' : get_recent_activity_chats(request)}
    return render(request, 'base/chats.html', context)


@login_required(login_url = 'login')
def show_chat_content(request, pk):
    chat_room = Chat.objects.get(id = pk)
    chat_content = chat_room.message_set.all()

    if request.user != chat_room.participant_1 and request.user != chat_room.participant_2:
        return redirect('show-chats')

    if request.method == 'POST':
        
        message_content = request.POST.get('message')

        message = Message.objects.create(

            chat = chat_room,
            owner = request.user,
            body = message_content

        )

        chat_room.recent_message = message_content
        chat_room.recent_message_owner = request.user.username
        chat_room.save()

        message.save()

        return redirect('chat-content', pk)
    
    participant = chat_room.participant_1 if chat_room.participant_1 != request.user else chat_room.participant_2


    context = { 

        'messages' : chat_content,
        'participant' : participant,
        'message_page' : True,
        'recent_activity_chats' : get_recent_activity_chats(request)

            }
    return render(request, 'base/chat.html', context)


@login_required(login_url = 'login')
def update_post_view(request, pk):
    post = Post.objects.get(id = pk)
    
    if request.method == "POST" and request.user == post.owner:
        description = request.POST.get('text')

        post.description = description

        post.save()

        return redirect('post', pk)


    context = {'recent_activity_chats' : get_recent_activity_chats(request)}
    return render(request, 'base/update-text.html', context)

@login_required(login_url = 'login')
def update_comment_view(request, pk):
    comment = Comment.objects.get(id = pk)
    post = Post.objects.get(comment = comment)

    if request.method == "POST" and request.user == comment.owner:
        content = request.POST.get('text')

        comment.body = content

        comment.save()

        return redirect('post', post.id)
    
    
    context = {'recent_activity_chats' : get_recent_activity_chats(request)}
    return render(request, 'base/update-text.html', context)


@login_required(login_url = "login")
def update_message_view(request, pk):
    message = Message.objects.get(id = pk)
    chat = message.chat

    if request.method == "POST" and request.user == message.owner:
        content = request.POST.get('text')

        message.body = content
        chat.recent_message = content
        chat.recent_message_owner = request.user.username

        message.save()
        chat.save()

        return redirect('chat-content', message.chat.id)
    
    context = {'recent_activity_chats' : get_recent_activity_chats(request)}
    return render(request, 'base/update-text.html', context)