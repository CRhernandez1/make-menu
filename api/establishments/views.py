import json
from json.decoder import JSONDecodeError

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import get_instance_or_404, require_http_methods

from .models import Establishment, Table
from .serializers import EstablishmentSerializer, TableSerializer


def establishments_list(request):
    establishments = Establishment.objects.all()
    return EstablishmentSerializer(establishments).json_response()


# Tables Views
@require_http_methods('GET')
@get_instance_or_404(Establishment, 'cif', 'Establishment')
def tables_list(request, establishment_cif):
    establishment = request.instance
    tables = establishment.tables.all()
    return TableSerializer(tables).json_response()


@require_http_methods('GET')
@get_instance_or_404(Establishment, 'cif', 'Establishment')
def table_detail(request, establishment_cif, table_num):
    establishment = request.instance
    try:
        table = establishment.tables.get(number=table_num)
    except Table.DoesNotExist:
        return JsonResponse({'message': 'Table not found!'}, status=404)
    return TableSerializer(table).json_response()


@csrf_exempt
@require_http_methods('POST')
@get_instance_or_404(Establishment, 'cif', 'Establishment')
def edit_table(request, establishment_cif, table_num):
    establishment = request.instance

    try:
        table = establishment.tables.get(number=table_num)
    except Table.DoesNotExist:
        return JsonResponse({'message': 'Table not found!'}, status=404)

    try:
        payload = json.loads(request.body)
    except JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON!'})

    try:
        max_guests = payload['max_guests']
    except KeyError:
        return JsonResponse({'message': 'This field is required.'})

    table.max_guests = max_guests
    table.save()
    return JsonResponse(
        {'message': f'Table {table.number} updated to {table.max_guests} guests.'}, status=200
    )


@csrf_exempt
@require_http_methods('POST')
@get_instance_or_404(Establishment, 'cif', 'Establishment')
def add_table(request, establishment_cif):
    establishment = request.instance

    try:
        payload = json.loads(request.body)
    except JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON!'})

    try:
        number = payload['number']
        max_guests = payload['max_guests']
    except KeyError:
        return JsonResponse({'message': 'This field is required.'})

    if not isinstance(max_guests, int):
        return JsonResponse({'message': 'Max guests must be a integer.'})

    if not isinstance(number, int):
        return JsonResponse({'message': 'Number must be an integer.'}, status=400)

    table = Table.objects.create(establishment=establishment, number=number, max_guests=max_guests)
    return JsonResponse({'id': table.pk}, status=201)


@csrf_exempt
@require_http_methods('GET')
@get_instance_or_404(Establishment, 'cif', 'Establishment')
def change_table_status(request, establishment_cif, table_num):
    establishment = request.instance

    try:
        table = establishment.tables.get(number=table_num)
    except Table.DoesNotExist:
        return JsonResponse({'message': 'Table not found!'}, status=404)

    table.active = not table.active
    table.save()
    return TableSerializer(table).json_response()


@csrf_exempt
@require_http_methods('GET')
@get_instance_or_404(Establishment, 'cif', 'Establishment')
def delete_table(request, establishment_cif, table_num):
    establishment = request.instance

    try:
        table = establishment.tables.get(number=table_num)
    except Table.DoesNotExist:
        return JsonResponse({'message': 'Table not found!'}, status=404)

    table.delete()
    return JsonResponse({'message': 'Table delete succesfully'}, status=204)
