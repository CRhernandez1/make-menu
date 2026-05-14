import django_rq

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

from .models import Member, Token
from .tasks import send_manager_email_task

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, raw=False, **kwargs):
    if not raw and created:
        Member.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_user_token(sender, instance, created, raw=False, **kwargs):
    if not raw and created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def send_email_after_manager_creation(sender, instance, raw=False, **kwargs):
    if raw:
        return

    if instance.is_superuser:
        return

    if not instance.is_staff:
        return

    if not instance.email:
        return

    try:
        member = instance.member
    except Member.DoesNotExist:
        return

    if member.manager_email_sent:
        return

    temporary_password = get_random_string(12)

    instance.set_password(temporary_password)
    User.objects.filter(pk=instance.pk).update(password=instance.password)

    queue = django_rq.get_queue("default")
    queue.enqueue(send_manager_email_task, instance.pk, temporary_password)