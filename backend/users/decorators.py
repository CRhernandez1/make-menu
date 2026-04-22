from http import HTTPStatus

from django.http import JsonResponse

from .models import Token


def auth_required(func):
    def wrapper(request, *args, **kwargs):
        token_value = request.COOKIES.get('auth_token')
        if not token_value:
            return JsonResponse(
                {'error': 'Authentication required'}, status=HTTPStatus.UNAUTHORIZED
            )
        try:
            token = Token.objects.get(key=token_value)
        except (Token.DoesNotExist, ValueError):
            return JsonResponse(
                {'error': 'Invalid authentication token'}, status=HTTPStatus.UNAUTHORIZED
            )
        if token.is_expired():
            token.delete()
            return JsonResponse({'error': 'Token expired'}, status=HTTPStatus.UNAUTHORIZED)
        request.user = token.user
        return func(request, *args, **kwargs)

    return wrapper
