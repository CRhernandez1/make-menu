from establishments.serializers import EstablishmentSerializer, TableSerializer
from products.serializers import ProductSerializer
from shared.serializers import BaseSerializer


class OrderSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:

        return {
            'id': instance.pk,
            'status': instance.status_get_display(),
            'table': TableSerializer(instance.table).serialize(),
            'establishment': EstablishmentSerializer(instance.establishment).serialize(),
            'placed_at': instance.placed_at.isoformat(),
            'paid': instance.paid,
            'total': float(instance.total),
            'closed_at': instance.closed_at.isoformat(),
        }


class OrderDetailSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:

        return {
            'id': instance.pk,
            'order': OrderSerializer(instance.order).serialize(),
            'product': ProductSerializer(instance.product, request=self.request).serialize(),
            'price': float(instance.price),
            'notes': instance.notes,
            'quantity': instance.quantity,
        }
