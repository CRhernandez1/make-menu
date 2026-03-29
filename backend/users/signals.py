from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Member, Token

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, raw, **kwargs):
    if not raw and created:
        Member.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_user_token(sender, instance, created, raw, **kwargs):
    if not raw and created:
        Token.objects.create(user=instance)
