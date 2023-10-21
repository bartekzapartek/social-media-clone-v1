from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    following = models.ManyToManyField(User, blank = True, null = True, related_name = 'user_profile_following')
    followers = models.ManyToManyField(User, blank = True, null = True, related_name = 'user_profile_followers')

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name = 'post_likes')

    description = models.TextField()

    created = models.DateTimeField(auto_now = True)
    updated = models.DateTimeField(auto_now_add = True)


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)

    body = models.TextField(blank = False, null = False)

    created = models.DateTimeField(auto_now = True)
    updated = models.DateTimeField(auto_now_add = True)
