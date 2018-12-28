from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    nickname = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='avatars', default='avatars/info.png')

    def __str__(self):
        return self.username