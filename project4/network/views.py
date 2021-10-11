import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import *
from datetime import datetime
from django.core.paginator import Paginator


class NewPostForm(forms.Form):
    topic = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'id': 'post-title', 
        'placeholder': 'Topic',
        }))
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'id': 'post-textarea', 
        'placeholder': 'Content',
        }))

def index(request):
    posts = Post.objects.all()
    liked_posts = []

    posts = posts.order_by('-creation_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    try:
        liked_posts = Post.objects.filter(likes=request.user)
    except:
        print('No liked posts')

    return render(request, "network/index.html", {
        "title": "All Posts",
        "posts": posts,
        "index": 'True',
        "liked_posts": liked_posts,
        "postForm": NewPostForm(),
        "page_obj": page_obj,
        "range": range(page_obj.paginator.num_pages)
    })
 
def login_view(request):
    next_page = None
    try:
        next_page = request.GET['next']
    except:
        print("next is not provided")

    if request.method == "POST":            

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if next_page is not None:
                return HttpResponseRedirect(next_page)
            else:
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url='login')
def following(request):

    user = request.user
    followings = []
    posts = Post.objects.none()
    liked_posts = []

    try:
        liked_posts = Post.objects.filter(likes=request.user)
    except:
        print('No liked posts')

    try:
        followings = user.followings.all()
    except:
        followings = ''

    if followings:
        for user in followings:
            followings_posts = Post.objects.filter(creator__username=user)            
            posts = posts | followings_posts

    posts = posts.order_by('-creation_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "title": "Following",
        "posts": posts,
        "liked_posts": liked_posts,
        "page_obj": page_obj,
        "range": range(page_obj.paginator.num_pages)
    })

def user(request, user):

    profile_owner = User.objects.get(username=user)
    liked_posts = []
    owner_followers = []
    follow = ''  

    try:
        liked_posts = Post.objects.filter(likes=request.user)
    except:
        print('No liked posts')

    try:
        followers = profile_owner.followers.all()
    except:
        print('No followers')
    
    if request.user in followers:
        follow = 'True'

    posts = []
    try:      
        posts = Post.objects.filter(creator__username=user)
        user = User.objects.get(username=user)
        posts = posts.order_by('-creation_date')
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)     
        
    except:
        return render(request, "network/index.html", {
            "title": "No Posts",
            "posts": posts,
            "user_": "True",
            "requested_user": user,
            'follow': follow,
            "liked_posts": liked_posts
        })

    return render(request, "network/index.html", {
        "title": f"{user} Posts",
        "posts": posts.order_by('-creation_date'),
        "user_": "True",
        "requested_user": user,
        'follow': follow,
        "liked_posts": liked_posts,
        "page_obj": page_obj,
        "range": range(page_obj.paginator.num_pages)
    })

def newPost(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)

        if form.is_valid():
            new_post = Post()
            new_post.creator = request.user
            new_post.title = form.cleaned_data["topic"]
            new_post.content = form.cleaned_data["content"]
            new_post.save()

    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
def follow(request, user):

    if not request.user.is_authenticated:
        return JsonResponse({
            "error": "You have to be logged in."
        }, status=400)

    if request.method == "PUT":
        user_to_follow = User.objects.get(username=user)
        user = request.user
        followers = []
        try:
            followers = user_to_follow.followers.all()
        except:
            print('No followers')
        
        if user not in followers:
            user_to_follow.followers.add(user)
            user.followings.add(user_to_follow)
        else:
            user_to_follow.followers.remove(user)
            user.followings.remove(user_to_follow)

        return HttpResponse(status=204)

    # Follow must be via PUT
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

@csrf_exempt
def like(request, post_id):

    if not request.user.is_authenticated:
        return JsonResponse({
            "error": "You have to be logged in."
        }, status=400)

    if request.method == "PUT":
        post_to_follow = Post.objects.get(id=post_id)
        user = request.user
        likes = []
        try:
            likes = post_to_follow.likes.all()
        except:
            print('No likes')
        
        if user not in likes:
            post_to_follow.likes.add(user)
        else:
            post_to_follow.likes.remove(user)

        return HttpResponse(status=204)

    # Like must be via PUT
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

@csrf_exempt
def edit(request, post_id):

    if not request.user.is_authenticated:
        return JsonResponse({
            "error": "You have to be logged in."
        }, status=400)

    if request.method == "PUT":
        post_to_edit = Post.objects.get(id=post_id)
            
        data = json.loads(request.body)
        if data.get("title") is not None:
            post_to_edit.title = data["title"]
        if data.get("content") is not None:
            post_to_edit.content = data["content"]
        post_to_edit.edit_date = datetime.now()
        post_to_edit.save()

        return HttpResponse(status=204)

    # Like must be via PUT
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)
