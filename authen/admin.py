from django.contrib import admin
from base.models import UserProfile, Post, Comment


admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)