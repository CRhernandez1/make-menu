from http import HTTPStatus

from django.http import JsonResponse


def require_http_methods(*methods):
    def my_decorator(view):
        def wrapper(request, *args, **kwargs):
            if request.method not in methods:
                return JsonResponse(
                    {'error': 'Method not allowed'}, status=HTTPStatus.METHOD_NOT_ALLOWED
                )
            return view(request, *args, **kwargs)

        return wrapper

    return my_decorator


def get_instance_or_404(model, field_name, instance_name):
    def my_decorator(view):
        def wrapper(request, *args, **kwargs):
            try:
                search_value = next(iter(kwargs.values()))
            except StopIteration:
                return JsonResponse({'error': 'URL param missing'}, status=HTTPStatus.BAD_REQUEST)

            # Para que el get pueda interpretar el field_name como un campo de
            # la base de datos, y no una string literal, hay que pasarlo
            # en forma de diccionario
            filters = {field_name: search_value}
            try:
                request.instance = model.objects.get(**filters)
            except model.DoesNotExist:
                return JsonResponse(
                    {'error': f'{instance_name.capitalize()} not found'},
                    status=HTTPStatus.NOT_FOUND,
                )
            return view(request, *args, **kwargs)

        return wrapper

    return my_decorator
