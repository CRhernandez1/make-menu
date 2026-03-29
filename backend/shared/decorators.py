import json
from http import HTTPStatus

from django.http import JsonResponse


def require_http_methods(*methods):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.method not in methods:
                return JsonResponse(
                    {'error': 'Method not allowed'},
                    status=HTTPStatus.METHOD_NOT_ALLOWED,
                )
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def parse_json_to_python(*expected_fields):
    def my_decorator(view):
        def wrapper(request, *args, **kwargs):
            try:
                payload = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON body'}, status=HTTPStatus.BAD_REQUEST)

            try:
                for field in expected_fields:
                    payload[field]
            except KeyError:
                return JsonResponse(
                    {'error': 'Missing required fields'},
                    status=HTTPStatus.BAD_REQUEST,
                )

            request.payload = payload
            return view(request, *args, **kwargs)

        return wrapper

    return my_decorator
