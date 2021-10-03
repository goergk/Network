from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *


def index(request):
    posts = Post.objects.all()

    try:
        Post.objects.filter(likes=request.user)
        liked_post='True'
    except:
        liked_post='False'

    return render(request, "network/index.html", {
        "title": "All Posts",
        "posts": posts,
        "index": 'True',
        "liked_post": liked_post
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
    return render(request, "network/index.html", {
        "title": "Following"
    })

def user(request, user):

    posts = []
    try:
        print(f"{user}")        
        posts = Post.objects.filter(creator__username=user)
        user = User.objects.get(username=user)     
        
    except:
        return render(request, "network/index.html", {
            "title": "No Posts",
            "posts": posts,
            "user_": "True",
            "requested_user": user
        })

    return render(request, "network/index.html", {
        "title": f"{user} Posts",
        "posts": posts,
        "user_": "True",
        "requested_user": user
    })