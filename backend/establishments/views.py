import json
from http import HTTPStatus

from django.http import JsonResponse

from shared.decorators import require_http_methods
from users.decorators import auth_required

from .models import Invitation, Manage


@require_http_methods('POST')
@auth_required
def generate_invitation(request):
    try:
        # 1. Leer el rol que nos pide Vue (si no envían nada, por defecto es WAITER)
        try:
            body = json.loads(request.body)
            role_requested = body.get('role', Manage.Role.WAITER)
        except json.JSONDecodeError:
            role_requested = Manage.Role.WAITER

        # 2. SEGURIDAD VITAL: Verificar que el usuario que hace la petición es MANAGER
        # Buscamos si el request.user tiene una entrada en Manage con el rol MANAGER
        try:
            manager_link = Manage.objects.get(member=request.user, role=Manage.Role.MANAGER)
            establishment = manager_link.establishment
        except Manage.DoesNotExist:
            return JsonResponse(
                {
                    'error': 'Acceso denegado. No tienes permisos de Manager en ningún establecimiento.'
                },
                status=HTTPStatus.FORBIDDEN,
            )

        # 3. Fabricar la invitación secreta en la base de datos
        invitation = Invitation.objects.create(
            establishment=establishment, role=role_requested, created_by=request.user
        )

        # 4. Devolver el UUID al frontend para que dibuje el QR
        return JsonResponse(
            {
                'message': 'Pase VIP generado correctamente',
                'invitation_id': str(invitation.id),
                'role': invitation.role,
                'establishment_name': establishment.name,
            },
            status=HTTPStatus.CREATED,
        )

    except Exception as e:
        return JsonResponse(
            {'error': f'Error interno del servidor: {str(e)}'},
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
