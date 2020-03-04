from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name = 'user', on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name = 'follower',symmetrical=False)

    def __str__(self):
        return self.user.username
