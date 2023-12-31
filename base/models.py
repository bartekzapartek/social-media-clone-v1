from django.db import models
from django.contrib.auth.models import User

from uuid import uuid4

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    following = models.ManyToManyField(User, blank = True, null = True, related_name = 'user_profile_following')
    followers = models.ManyToManyField(User, blank = True, null = True, related_name = 'user_profile_followers')




def rename(instance, filename):
    ext = filename.split('.')[-1]

    return f'covers/{instance.owner.username}_{uuid4().hex}.{ext}'


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name = 'post_likes')

    cover = models.ImageField(upload_to = rename, null = True, blank = True)
    description = models.TextField()

    created = models.DateTimeField(auto_now = True)
    updated = models.DateTimeField(auto_now_add = True)


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)

    body = models.TextField(blank = False, null = False)

    created = models.DateTimeField(auto_now = True)
    updated = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ["-created"]



class Chat(models.Model):
    participant_1 = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'participant_1')
    participant_2 = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'participant_2')

    recent_message_owner = models.TextField(blank = True, null = True, default = '')
    recent_message = models.TextField(blank = True, null = True, default = '')

    created = models.DateTimeField(auto_now = True)
    updated = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering = ['-created', '-updated']


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete = models.CASCADE)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)

    body = models.TextField(blank = False, null = False)

    created = models.DateField(auto_now = True)
    updated = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-created', '-updated']