from django.contrib import admin
from .models import Profile, Post, LikePost
# Register your models here.

# Username : picpod
# Email address: admin@picpod.com
# pass: picpod

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)

