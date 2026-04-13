from users.serializers import MemberSerializer

from shared.serializers import BaseSerializer


class EstablishmentSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'legal_name': instance.legal_name,
            'cif': instance.cif,
            'description': instance.description,
            'zip_code': instance.zip_code,
            'city': instance.city,
            'address': instance.address,
            'phone': instance.phone,
            'opened': instance.opened,
        }


class TableSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'establishment': EstablishmentSerializer(instance.establishment).serialize(),
            'max_guests': instance.max_guests,
            'active': instance.active,
        }


from users.serializers import UserSerializer
from shared.serializers import BaseSerializer

class EstablishmentSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'legal_name': instance.legal_name,
            'cif': instance.cif,
            'description': instance.description,
            'zip_code': instance.zip_code,
            'city': instance.city,
            'address': instance.address,
            'phone': instance.phone,
            'opened': instance.opened,
        }

class TableSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'establishment': EstablishmentSerializer(instance.establishment).serialize(),
            'number': instance.number,
            'max_guests': instance.max_guests,
            'active': instance.active,
        }

class ManageSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'member': UserSerializer(instance.member).serialize(),
            'role': instance.role,
            'joined_at': str(instance.joined_at),
            'end_date': str(instance.end_date) if instance.end_date else None,
        }
