from establishments.serializers import EstablishmentSerializer
from shared.serializers import BaseSerializer


class ProductSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:

        return {
            'id': instance.pk,
            'establishment': EstablishmentSerializer(instance.establishment).serialize(),
            'category': CategorySerializer(instance.category).serialize(),
            'name': instance.name,
            'description': instance.description,
            'product_image': self.build_url(instance.product_image.url),
            'price': float(instance.price),
            'available': instance.available,
        }


class IngredientSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:

        return {
            'id': instance.pk,
            'establishment': EstablishmentSerializer(instance.establishment).serialize(),
            'allergens': AllergenSerializer(
                instance.allergens.all(), request=self.request
            ).serialize(),
            'ingredient_type': instance.get_ingredient_type_display(),
            'name': instance.name,
            'description': instance.description,
            'available': instance.available,
        }


class ComponentSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:

        return {
            'id': instance.pk,
            'product': ProductSerializer(instance.product, request=self.request).serialize(),
            'ingredient': IngredientSerializer(instance.ingredient).serialize(),
            'quantity': float(instance.quantity),
            'unity': instance.get_unity_display(),
            'removable': instance.removable,
        }


class AllergenSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:

        return {
            'id': instance.pk,
            'name': instance.name,
            'icon': self.build_url(instance.icon.url),
        }


class CategorySerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:

        return {
            'id': instance.pk,
            'establishment': EstablishmentSerializer(instance.establishment).serialize(),
            'name': instance.name,
        }
