from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    owner = models.OneToOneField(User, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name = 'users_likes')

    description = models.TextField()

    created = models.DateTimeField(auto_now = True)
    updated = models.DateTimeField(auto_now_add = True)


class Comment(models.Model):
    owner = models.OneToOneField(User, on_delete = models.CASCADE)
    post = models.OneToOneField(Post, on_delete = models.CASCADE)

    body = models.TextField(blank = False, null = False)

    created = models.DateTimeField(auto_now = True)
    updated = models.DateTimeField(auto_now_add = True)
