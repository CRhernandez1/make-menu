import json
from functools import wraps
from http import HTTPStatus
from django.http import JsonResponse
from establishments.models import Manage

def require_http_methods(*methods):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if request.method not in methods:
                return JsonResponse(
                    {'error': 'Method not allowed'},
                    status=HTTPStatus.METHOD_NOT_ALLOWED,
                )
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

def get_instance_or_404(model, field, label):
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            field_value = kwargs.get(f'{label.lower()}_{field}')
            try:
                request.instance = model.objects.get(**{field: field_value})
            except model.DoesNotExist:
                return JsonResponse(
                    {'error': f'{label} not found.'},
                    status=HTTPStatus.NOT_FOUND,
                )
            return view(request, *args, **kwargs)
        return wrapper
    return decorator

def require_role(role=None):
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            filters = {'establishment': request.instance}
            if role:
                filters['role'] = role
            if not request.user.manages.filter(**filters).exists():
                return JsonResponse(
                    {'error': 'No tienes permiso para esta acción.'},
                    status=HTTPStatus.FORBIDDEN,
                )
            return view(request, *args, **kwargs)
        return wrapper
    return decorator

def parse_json(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        try:
            request.payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body'}, status=HTTPStatus.BAD_REQUEST)
        return view(request, *args, **kwargs)
    return wrapper