from shared.serializers import BaseSerializer
from users.serializers import MemberSerializer


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


class ManageSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'establishment': EstablishmentSerializer(instance.establishment).serialize(),
            'member': MemberSerializer(instance.member, request=self.request).serialize(),
            'role': instance.get_role_display(),
            'joined_at': instance.joined_at.isoformat(),
            'end_date': instance.end_date.isoformat(),
        }
