
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
    path("user/<str:user>/follow", views.follow, name="follow"),
    path("user/post/like/<int:post_id>", views.like, name="like"),
    path("post/like/<int:post_id>", views.like, name="like"),
    path("edit/<int:post_id>", views.edit, name="edit")
]
