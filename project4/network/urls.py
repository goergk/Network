
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("newPost", views.newPost, name="newPost"),
    path("user/<str:user>", views.user, name="user"),
    
    # API Routes
    path("user/<str:user>/follow", views.follow, name="follow")
]
