from shared.serializers import BaseSerializer


class OrderSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'status': instance.status,
            'status_display': instance.get_status_display(),
            'table_number': instance.table.number if instance.table else None,
            'establishment_name': instance.establishment.name if instance.establishment else None,
            'placed_at': instance.placed_at.isoformat(),
            'paid': instance.paid,
            'total': '{:.2f}'.format(instance.total),
            'closed_at': instance.closed_at.isoformat() if instance.closed_at else None,
        }


class OrderDetailSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'product_name': instance.product.name if instance.product else None,
            'price': '{:.2f}'.format(instance.price),
            'notes': instance.notes,
            'quantity': instance.quantity,
        }
