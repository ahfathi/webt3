from django.db import models
from users.models import User

# Create your models here.

class AccessKey(models.Model):
    token = models.CharField(max_length=64, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token