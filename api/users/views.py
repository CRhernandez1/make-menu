import json

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import require_http_methods

from .models import Member, Token


@csrf_exempt
@require_http_methods('POST')
def auth(request):
    payload = json.loads(request.body)

    username = payload['username']
    password = payload['password']

    if user := authenticate(username=username, password=password):
        Token.objects.get_or_create(user=user)
        return JsonResponse({'token': user.token.key})

    return JsonResponse({'error': 'Invalid credentials'}, status=401)


@csrf_exempt
@require_http_methods('POST')
def register(request):
    payload = json.loads(request.body)

    username = payload['username']
    password = payload['password']
    first_name = payload['first_name']
    last_name = payload['last_name']
    email = payload['email']
    phone = payload['phone']
    # avatar = payload['avatar']

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Name currently in use'}, status=400)

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )

    Member.objects.create(user=user, phone=phone)

    return JsonResponse({'message': 'User created successfully'}, status=201)
