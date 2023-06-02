from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    email = models.EmailField(max_length=50, blank=True)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    porfile_img = models.ImageField(upload_to='profile_images', default='blank-profile-picture.jpg')
    background = models.ImageField(upload_to='background_images', default='timeline-1.jpg')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    perfil = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    posted_at = models.DateTimeField(default=datetime.now)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user
    
class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)