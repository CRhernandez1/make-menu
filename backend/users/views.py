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
        return JsonResponse({'error': 'Username and password are required.'}, status=HTTPStatus.BAD_REQUEST)

    if user := authenticate(username=username, password=password):
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({'token': str(token.key)}, status=HTTPStatus.OK)
    return JsonResponse({'error': 'Invalid credentials'}, status=HTTPStatus.UNAUTHORIZED)


@csrf_exempt
@require_http_methods('POST')
@parse_json
def register(request):
    required = ['username', 'password', 'email', 'first_name', 'last_name', 'invitation_id']
    missing = [f for f in required if not request.payload.get(f)]
    if missing:
        return JsonResponse({'error': f'Missing required fields: {", ".join(missing)}'}, status=HTTPStatus.BAD_REQUEST)

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
    return JsonResponse({'message': 'Logged out successfully'}, status=HTTPStatus.OK)


@require_http_methods('GET')
@auth_required
def profile(request):
    return MemberSerializer(request.user.member, request=request).json_response()
