from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followings = models.ManyToManyField('User', related_name="user_followings", blank=True, symmetrical=False)
    followers = models.ManyToManyField('User', related_name="user_followers", blank=True, symmetrical=False)
    pass

class Post(models.Model):
    creator =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_creator")
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=2500)
    creation_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)


