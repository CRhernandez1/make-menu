import uuid
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class Member(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='member', on_delete=models.CASCADE
    )
    phone = models.CharField(max_length=16, blank=True)
    avatar = models.ImageField(upload_to='avatar', default='avatar/noavatar.png')
    manager_email_sent = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Member: {self.user.username}'


class Token(models.Model):
    key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='token', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=30)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def refresh(self, long_lived=False):
        """Regenera key y expiración. long_lived=True → 30 días, False → 12 horas."""
        self.key = uuid.uuid4()
        duration = timedelta(days=30) if long_lived else timedelta(hours=12)
        self.expires_at = timezone.now() + duration
        self.save()

    def __str__(self):
        return str(self.key)
