from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models
from users.models import User

# Create your models here.

class AccessKey(models.Model):
    token = models.CharField(max_length=64, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token



@receiver(post_save, sender=User)
def handle_new_user(instance, created, **kwargs):
    if created:
        key = AccessKey(user=instance)
        key.save()