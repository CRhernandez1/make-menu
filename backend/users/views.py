from http import HTTPStatus

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from establishments.models import Invitation, Manage
from shared.decorators import parse_json_to_python, require_http_methods
from users.decorators import auth_required
from users.models import Token

from .serializers import MemberSerializer


@csrf_exempt
@require_http_methods('POST')
@parse_json_to_python('username', 'password')
def login(request):
    username = request.payload['username']
    password = request.payload['password']

    if user := authenticate(username=username, password=password):
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({'token': str(token.key)}, status=HTTPStatus.OK)
    return JsonResponse({'error': 'Invalid credentials'}, status=HTTPStatus.UNAUTHORIZED)


@csrf_exempt
@require_http_methods('POST')
@parse_json_to_python('username', 'password', 'email', 'first_name', 'last_name', 'invitation_id')
def register(request):
    try:
        # 1. Validar la invitación ANTES de crear el usuario
        invitation_id = request.payload.get('invitation_id')
        try:
            invitation = Invitation.objects.get(id=invitation_id, is_used=False)
        except (Invitation.DoesNotExist, ValidationError):
            return JsonResponse(
                {'error': 'Invitación inválida o ya usada'}, status=HTTPStatus.BAD_REQUEST
            )

        # 2. Crear el usuario (esto ya lo tenías)
        user = User.objects.create_user(
            username=request.payload['username'],
            password=request.payload['password'],
            email=request.payload['email'],
            first_name=request.payload['first_name'],
            last_name=request.payload['last_name'],
        )

        if 'phone' in request.payload:
            user.member.phone = request.payload['phone']
            user.member.save()

        # 3. LA CLAVE: Crear el rol en el restaurante de la invitación
        Manage.objects.create(
            establishment=invitation.establishment, member=user, role=invitation.role
        )

        # 4. Quemar la invitación para que no se use dos veces
        invitation.is_used = True
        invitation.save()

        return JsonResponse(
            {'message': 'Registro completado y vinculado al restaurante'}, status=HTTPStatus.CREATED
        )

    except IntegrityError:
        return JsonResponse({'error': 'El nombre de usuario ya existe'}, status=HTTPStatus.CONFLICT)


@csrf_exempt
@require_http_methods('POST')
@auth_required
def logout(request):
    request.user.token.delete()
    return JsonResponse({'message': 'Logged out successfully'}, status=HTTPStatus.OK)


@require_http_methods('GET')
@auth_required
def profile(request):
    return MemberSerializer(request.user.member, request=request).json_response()
