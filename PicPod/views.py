from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost
# from itertools import chain
import random

#index view
@login_required(login_url='signin')
def index(req):
    user_object = User.objects.get(username=req.user.username)
    user_profile = Profile.objects.get(user=user_object)

    posts = Post.objects.all()
    return render(req, 'index.html', {'user_profile':user_profile, 'posts':posts})


#upload view
@login_required(login_url='signin')
def upload(req):
    if req.method == "POST":
        user = req.user.username
        image = req.FILES.get('image_upload')
        caption = req.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')

    else:    
        return redirect('/')


#like post view
@login_required(login_url='signin')
def like_post(req):
    username = req.user.username
    post_id = req.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')


#settings view
@login_required(login_url='signin')
def settings(req):
    user_profile = Profile.objects.get(user=req.user)

    if req.method == 'POST':
        
        if req.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = req.POST['bio']
            location = req.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if req.FILES.get('image') != None:
            image = req.FILES.get('image')
            bio = req.POST['bio']
            location = req.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('settings')
    return render(req, 'setting.html', {'user_profile': user_profile})


#signup view
def signup(req):
    if req.method == 'POST':
        username = req.POST['username']
        email = req.POST['email']
        password = req.POST['password']
        password2 = req.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(req, 'Email already exists.')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(req, 'Username already exists.')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password = password)
                auth.login(req, user_login)

                #create a Profile object for new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user = user_model.id)
                new_profile.save();
                return redirect('setting')
        else:
            messages.info(req, 'Passwords did not match!')
            return redirect('signup')

    else:    
        return render(req, 'signup.html')
    

#signin view
def signin(req):
    
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(req, user)
            return redirect('/')
        else:
            messages.info(req, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(req, 'signin.html')


#logout view
@login_required(login_url='signin')
def logout(req):
    auth.logout(req)
    return redirect('signin')