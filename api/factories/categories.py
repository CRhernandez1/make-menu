import factory

from .establishments import EstablishmentFactory


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'products.Category'  # Tu modelo

    # Si no se lo pasamos nosotros, creará uno nuevo (SubFactory).
    # PERO nosotros se lo pasaremos manualmente en el script.
    establishment = factory.SubFactory(EstablishmentFactory)
    name = factory.Faker('word')
