from shared.serializers import BaseSerializer


class UserSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'username': instance.username,
            'email': instance.email,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
        }


class MemberSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        # 1. Cruzamos el puente hacia Manage usando el related_name='manages'
        # Filtramos por end_date__isnull=True para asegurarnos de coger su puesto actual
        active_manage = instance.user.manages.filter(end_date__isnull=True).first()
        user_role = active_manage.role if active_manage else None
        establishment = active_manage.establishment if active_manage else None

        return {
            'id': instance.pk,
            'user': UserSerializer(instance.user).serialize(),
            'phone': instance.phone,
            'avatar': self.build_url(instance.avatar.url) if instance.avatar else None,
            'role': user_role,
            'establishment_id': establishment.pk if establishment else None,
            'establishment_cif': establishment.cif if establishment else None,
        }
