import json
from http import HTTPStatus

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import get_instance_or_404, require_http_methods, require_role, parse_json

from users.decorators import auth_required

from .models import Establishment, Table, Manage, Invitation
from .forms import EstablishmentCreateForm, EstablishmentUpdateForm, TableCreateForm, TableUpdateForm, ManageUpdateForm

from .serializers import EstablishmentSerializer, TableSerializer, ManageSerializer


# ──────────────────────────────────────────────
# Establishment Views
# ──────────────────────────────────────────────

@csrf_exempt
@require_http_methods('GET')
@auth_required
def establishments_list(request):
    establishments = Establishment.objects.filter(manages__member=request.user)
    return EstablishmentSerializer(establishments).json_response()


@csrf_exempt
@require_http_methods('GET')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
def establishment_detail(request, establishment_cif):
    return EstablishmentSerializer(request.instance).json_response()


@csrf_exempt
@require_http_methods('POST')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
@parse_json
def edit_establishment(request, establishment_cif):
    form = EstablishmentUpdateForm(request.payload, instance=request.instance)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    form.save()
    return JsonResponse({'message': f'Establishment {request.instance.cif} updated!'}, status=200)


@csrf_exempt
@require_http_methods('POST')
@auth_required
@parse_json
def add_establishment(request):
    form = EstablishmentCreateForm(request.payload)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    establishment = form.save()
    Manage.objects.create(
        establishment=establishment,
        member=request.user,
        role=Manage.Role.MANAGER
    )
    return JsonResponse({'id': establishment.pk}, status=201)


@csrf_exempt
@require_http_methods('POST')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
def toggle_establishment(request, establishment_cif):
    request.instance.opened = not request.instance.opened
    request.instance.save()
    return EstablishmentSerializer(request.instance).json_response()


@csrf_exempt
@require_http_methods('POST')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
def delete_establishment(request, establishment_cif):
    request.instance.manages.all().delete()
    request.instance.delete()
    return JsonResponse({'message': 'Establishment deleted successfully.'}, status=204)


# ──────────────────────────────────────────────
# Table Views
# ──────────────────────────────────────────────

@csrf_exempt
@require_http_methods('GET')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role()
def tables_list(request, establishment_cif):
    tables = request.instance.tables.all()
    return TableSerializer(tables).json_response()


@csrf_exempt
@require_http_methods('GET')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role()
def table_detail(request, establishment_cif, table_num):
    try:
        table = request.instance.tables.get(number=table_num)
    except Table.DoesNotExist:
        return JsonResponse({'message': 'Table not found!'}, status=404)

    return TableSerializer(table).json_response()


@csrf_exempt
@require_http_methods('POST')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
@parse_json
def add_table(request, establishment_cif):
    form = TableCreateForm(request.payload)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    if request.instance.tables.filter(number=form.cleaned_data['number']).exists():
        return JsonResponse({'message': f'Table {form.cleaned_data["number"]} already exists.'}, status=409)

    table = form.save(commit=False)
    table.establishment = request.instance
    table.save()
    return JsonResponse({'id': table.pk}, status=201)


@csrf_exempt
@require_http_methods('POST')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
@parse_json
def edit_table(request, establishment_cif, table_num):
    try:
        table = request.instance.tables.get(number=table_num)
    except Table.DoesNotExist:
        return JsonResponse({'message': 'Table not found!'}, status=404)

    form = TableUpdateForm(request.payload, instance=table)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    form.save()
    return JsonResponse({'message': f'Table {table.number} updated to {table.max_guests} guests.'}, status=200)


@csrf_exempt
@require_http_methods('POST')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
def change_table_status(request, establishment_cif, table_num):
    try:
        table = request.instance.tables.get(number=table_num)
    except Table.DoesNotExist:
        return JsonResponse({'message': 'Table not found!'}, status=404)

    table.active = not table.active
    table.save()
    return TableSerializer(table).json_response()


@csrf_exempt
@require_http_methods('POST')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
def delete_table(request, establishment_cif, table_num):
    try:
        table = request.instance.tables.get(number=table_num)
    except Table.DoesNotExist:
        return JsonResponse({'message': 'Table not found!'}, status=404)

    table.delete()
    return JsonResponse({'message': 'Table deleted successfully.'}, status=204)


# ──────────────────────────────────────────────
# Staff Views
# ──────────────────────────────────────────────

@csrf_exempt
@require_http_methods('GET')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
def staff_list(request, establishment_cif):
    staff = request.instance.manages.select_related('member').all()
    return ManageSerializer(staff).json_response()


@csrf_exempt
@require_http_methods('POST')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
@parse_json
def edit_staff(request, establishment_cif, member_id):
    try:
        manage = request.instance.manages.get(member_id=member_id)
    except Manage.DoesNotExist:
        return JsonResponse({'message': 'Member not found!'}, status=404)

    if manage.member == request.user:
        return JsonResponse({'error': 'No puedes cambiar tu propio rol.'}, status=400)

    form = ManageUpdateForm(request.payload, instance=manage)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    form.save()
    return JsonResponse({'message': 'Role updated successfully.'}, status=200)


@csrf_exempt
@require_http_methods('POST')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
def remove_staff(request, establishment_cif, member_id):
    try:
        manage = request.instance.manages.get(member_id=member_id)
    except Manage.DoesNotExist:
        return JsonResponse({'message': 'Member not found!'}, status=404)

    if manage.member == request.user:
        return JsonResponse({'error': 'No puedes eliminarte a ti mismo.'}, status=400)

    manage.delete()
    return JsonResponse({'message': 'Member removed successfully.'}, status=204)


# ──────────────────────────────────────────────
# Invitation Views
# ──────────────────────────────────────────────


@require_http_methods('GET')
@auth_required
def my_establishments(request):
    manages = Manage.objects.filter(
        member=request.user, role=Manage.Role.MANAGER, end_date__isnull=True
    ).select_related('establishment')
    return JsonResponse(
        [
            {
                'id': m.establishment.id,
                'name': m.establishment.name,
                'cif': m.establishment.cif,
            }
            for m in manages
        ],
        safe=False,
    )


@csrf_exempt
@require_http_methods('POST')
@auth_required
def generate_invitation(request):
    try:
        # 1. Leer el rol que nos pide Vue (si no envían nada, por defecto es WAITER)
        try:
            body = json.loads(request.body)
            role_requested = body.get('role', Manage.Role.WAITER)
        except json.JSONDecodeError:
            role_requested = Manage.Role.WAITER

        # 2. SEGURIDAD VITAL: Verificar que el usuario que hace la petición es MANAGER
        # Buscamos si el request.user tiene una entrada en Manage con el rol MANAGER
        try:
            manager_link = Manage.objects.get(member=request.user, role=Manage.Role.MANAGER)
            establishment = manager_link.establishment
        except Manage.DoesNotExist:
            return JsonResponse(
                {
                    'error': 'Acceso denegado. No tienes permisos de Manager en ningún establecimiento.'
                },
                status=HTTPStatus.FORBIDDEN,
            )

        # 3. Fabricar la invitación secreta en la base de datos
        invitation = Invitation.objects.create(
            establishment=establishment, role=role_requested, created_by=request.user
        )

        # 4. Devolver el UUID al frontend para que dibuje el QR
        return JsonResponse(
            {
                'message': 'Pase VIP generado correctamente',
                'invitation_id': str(invitation.id),
                'role': invitation.role,
                'establishment_name': establishment.name,
            },
            status=HTTPStatus.CREATED,
        )

    except Exception as e:
        return JsonResponse(
            {'error': f'Error interno del servidor: {str(e)}'},
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@require_http_methods('GET')
def validate_invitation(request, invitation_id):
    try:
        invitation = Invitation.objects.get(id=invitation_id)

        # Usamos tu nueva función del modelo 🎯
        if not invitation.is_valid():
            return JsonResponse(
                {'valid': False, 'error': 'Esta invitación ya ha sido utilizada o ha caducado.'},
                status=400,
            )

        # Si es válida, le damos info útil para que el registro sea "personalizado"
        return JsonResponse(
            {
                'valid': True,
                'establishment_name': invitation.establishment.name,
                'role': invitation.role,
            },
            status=200,
        )

    except (Invitation.DoesNotExist, ValidationError):
        return JsonResponse(
            {'valid': False, 'error': 'El código de invitación no existe.'}, status=404
        )
