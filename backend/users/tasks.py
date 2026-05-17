from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from .models import Member

User = get_user_model()


def send_manager_email_task(user_id, temporary_password):
    user = User.objects.get(pk=user_id)

    login_url = f"{settings.FRONTEND_URL.rstrip('/')}/login"
    subject = "Bienvenido a MakeMenu"

    message = f"""
Hola {user.first_name or user.username},

Se ha creado tu cuenta de manager en MakeMenu.

Tus credenciales de acceso son:

Usuario: {user.username}
Email: {user.email}
Contraseña temporal: {temporary_password}

Accede en: {login_url}

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

    member = Member.objects.get(user=user)
    member.manager_email_sent = True
    member.save(update_fields=["manager_email_sent"])