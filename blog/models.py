from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    content = models.CharField(max_length = 200)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    post_connected = models.ForeignKey(Post, on_delete=models.CASCADE, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length = 200)

    def __str__(self):
        return self.content