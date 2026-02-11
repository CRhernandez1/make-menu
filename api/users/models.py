import uuid

from django.conf import settings
from django.db import models


class Member(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='member', on_delete=models.CASCADE
    )
    phone = models.CharField(max_length=16, blank=True)
    avatar = models.ImageField(upload_to='avatar', default='avatar/noavatar.png')

    def __str__(self):
        return self.user.first_name


class Token(models.Model):
    key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.key)
