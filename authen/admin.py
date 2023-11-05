from django.contrib import admin
from base.models import UserProfile, Post, Comment, Chat, Message


admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Chat)
admin.site.register(Message)