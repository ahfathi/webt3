from django.db import models
from users.models import User

# Create your models here.

class RequestData(models.Model):
    ip = models.GenericIPAddressField(db_index=True)
    user_agent = models.CharField(max_length=256)
    time = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, null=True)
    session_key = models.CharField(max_length=32, null=True)
    authorized = models.BooleanField(default=True)

    def __repr__(self):
        return '<%s: %s %s %s>' % (self.__class__.__name__, self.ip, self.user, self.session_key)

class BannedIP(models.Model):
    ip = models.GenericIPAddressField()
    time_banned = models.IntegerField()
    log = models.TextField()