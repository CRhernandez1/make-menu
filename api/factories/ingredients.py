import random

import factory

from factories.establishments import EstablishmentFactory
from products.models import Allergen, Ingredient


class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'products.Ingredient'

    name = factory.Faker('word')
    description = factory.Faker('sentence')

    # Tipo aleatorio
    ingredient_type = factory.Faker('random_element', elements=Ingredient.Type.values)

    # CAMBIO 1: Available al 90% (antes estaba siempre True)
    available = factory.Faker('boolean', chance_of_getting_true=90)

    # CAMBIO 2: Relación con Establishment
    # Lo dejamos como SubFactory. Esto significa: "Si no me das un restaurante, creo uno nuevo".
    # Pero tranquilo, en el script le daremos uno nosotros.
    establishment = factory.SubFactory(EstablishmentFactory)

    @factory.post_generation
    def allergens(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for allergen in extracted:
                self.allergens.add(allergen)
        else:
            todos = list(Allergen.objects.all())
            if todos:
                # 70% probabilidad de 0 alérgenos
                cantidad = random.choices([0, 1, 2], weights=[70, 20, 10], k=1)[0]
                if cantidad > 0:
                    seleccion = random.sample(todos, cantidad)
                    self.allergens.add(*seleccion)
