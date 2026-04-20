from http import HTTPStatus

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from establishments.models import Invitation, Manage
from shared.decorators import parse_json, require_http_methods
from users.decorators import auth_required
from users.models import Token

from .serializers import MemberSerializer


@csrf_exempt
@require_http_methods('POST')
@parse_json
def login(request):
    username = request.payload.get('username')
    password = request.payload.get('password')

    if not username or not password:
        return JsonResponse(
            {'error': 'Username and password are required.'}, status=HTTPStatus.BAD_REQUEST
        )

    user = authenticate(username=username, password=password)
    if not user:
        return JsonResponse({'error': 'Invalid credentials'}, status=HTTPStatus.UNAUTHORIZED)

    token, created = Token.objects.get_or_create(user=user)
    long_lived = request.payload.get('remember_me', False)
    token.refresh(long_lived=long_lived)

    # Respuesta con perfil completo (login + profile en una sola petición)
    profile_data = MemberSerializer(user.member, request=request).serialize()
    response = JsonResponse(profile_data)

    # Cookie HttpOnly — el frontend no puede leerla (protección XSS)
    max_age = 30 * 24 * 3600 if long_lived else None  # 30 días o cookie de sesión
    response.set_cookie(
        'auth_token',
        str(token.key),
        httponly=True,
        samesite='Lax',
        secure=False,  # Cambiar a True en producción con HTTPS
        max_age=max_age,
    )
    return response


@csrf_exempt
@require_http_methods('POST')
@parse_json
def register(request):
    required = ['username', 'password', 'email', 'first_name', 'last_name', 'invitation_id']
    missing = [f for f in required if not request.payload.get(f)]
    if missing:
        return JsonResponse(
            {'error': f'Missing required fields: {", ".join(missing)}'},
            status=HTTPStatus.BAD_REQUEST,
        )

    try:
        invitation_id = request.payload['invitation_id']
        try:
            invitation = Invitation.objects.get(id=invitation_id, is_used=False)
        except (Invitation.DoesNotExist, ValidationError):
            return JsonResponse(
                {'error': 'Invitación inválida o ya usada'}, status=HTTPStatus.BAD_REQUEST
            )

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

        Manage.objects.create(
            establishment=invitation.establishment, member=user, role=invitation.role
        )

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
    response = JsonResponse({'message': 'Logged out successfully'}, status=HTTPStatus.OK)
    response.delete_cookie('auth_token')
    return response


@require_http_methods('GET')
@auth_required
def profile(request):
    return MemberSerializer(request.user.member, request=request).json_response()
