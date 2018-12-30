from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    nickname = models.CharField(max_length=20, default='guest')
    avatar = models.ImageField(upload_to='avatars', default='avatars/info.png')

    def __str__(self):
        return self.nickname