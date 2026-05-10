from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

from .models import Member, Token

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, raw=False, **kwargs):
    if not raw and created:
        Member.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_user_token(sender, instance, created, raw=False, **kwargs):
    if not raw and created:
        Token.objects.create(user=instance)


def send_manager_email(user, password):
    if not user.email:
        return

    subject = "Bienvenido a MakeMenu"

    message = f"""
Hola {user.first_name or user.username},

Se ha creado tu cuenta de manager en MakeMenu.

Tus credenciales de acceso son:

Usuario: {user.username}
Email: {user.email}
Contraseña temporal: {password}

Accede en: http://localhost:5173/login

IMPORTANTE: cambia tu contraseña la primera vez que inicies sesión.

MakeMenu · Hecho en Tenerife
""".strip()

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


@receiver(post_save, sender=User)
def send_email_after_manager_creation(sender, instance, raw=False, **kwargs):
    if raw:
        return

    # Para que no mande email al superusuario admin:admin
    if instance.is_superuser:
        return

    # Usamos is_staff como equivalente de manager
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

    send_manager_email(instance, temporary_password)

    member.manager_email_sent = True
    member.save(update_fields=["manager_email_sent"])