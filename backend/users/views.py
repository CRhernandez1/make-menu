from http import HTTPStatus

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse

from shared.decorators import parse_json_to_python, require_http_methods
from users.models import Token


@require_http_methods('POST')
@parse_json_to_python('username', 'password')
def login(request):
    username = request.payload['username']
    password = request.payload['password']

    if user := authenticate(username=username, password=password):
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({'token': str(token.key)}, status=HTTPStatus.OK)
    return JsonResponse({'error': 'Invalid credentials'}, status=HTTPStatus.UNAUTHORIZED)


@require_http_methods('POST')
@parse_json_to_python('username', 'password', 'email', 'first_name', 'last_name')
def register(request):
    try:
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
        return JsonResponse({'message': 'User registered successfully'}, status=HTTPStatus.CREATED)

    except IntegrityError:
        return JsonResponse({'error': 'Username already exists'}, status=HTTPStatus.CONFLICT)


@require_http_methods('POST')
def logout(request):
    auth_header = request.headers.get('Authorization')

    if auth_header and auth_header.startswith('Bearer '):
        token_key = auth_header.split(' ')[1]

        try:
            token = Token.objects.get(key=token_key)
            token.delete()
            return JsonResponse({'message': 'Logged out successfully'}, status=HTTPStatus.OK)
        except Token.DoesNotExist:
            return JsonResponse(
                {'error': 'Token not found or already deleted'}, status=HTTPStatus.UNAUTHORIZED
            )
    return JsonResponse({'error': 'Invalid or missing token'}, status=HTTPStatus.UNAUTHORIZED)
