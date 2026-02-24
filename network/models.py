from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    contents = models.TextField(blank=True, default="")
    images = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']  # Newest first
    
    def __str__(self):
        return f"{self.owner.username}: {self.contents[:30]}..."

    

class Like(models.Model):
    # TODO:
    pass

class Follower(models.Model):
    # TODO:
    pass
