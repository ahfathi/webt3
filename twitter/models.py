from django.db import models
from users.models import User

class Post(models.Model):
	title = models.CharField(max_length=32)
	text = models.CharField(max_length=140)
	author = models.ForeignKey(User, on_delete='CASCADE')
	date_created = models.DateTimeField(auto_now_add=True)