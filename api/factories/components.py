import factory

from factories.ingredients import IngredientFactory
from factories.products import ProductFactory
from products.models import Component


class ComponentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'products.Component'

    # Estos SubFactory son solo "por si acaso" (si usas la factory vacía).
    # Como nosotros le pasaremos los datos en el script, NO se ejecutarán.
    product = factory.SubFactory(ProductFactory)
    ingredient = factory.SubFactory(IngredientFactory)

    # Cantidad aleatoria (10 a 200)
    quantity = factory.Faker('random_int', min=10, max=200)

    # Unidad aleatoria
    unity = factory.Faker('random_element', elements=Component.Unity.values)

    # 40% de probabilidad de que se pueda quitar el ingrediente
    removable = factory.Faker('boolean', chance_of_getting_true=40)
