import random

import factory

from factories.establishments import EstablishmentFactory


class TableFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'establishments.Table'

    # Capacidad variada para que el mapa de mesas no sea monótono
    max_guests = factory.LazyFunction(lambda: random.choice([2, 2, 4, 4, 4, 6, 8]))

    # CAMBIO: 95% de probabilidad de estar activa
    active = factory.Faker('boolean', chance_of_getting_true=95)

    establishment = factory.SubFactory(EstablishmentFactory)
