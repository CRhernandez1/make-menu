import random

import factory

from factories.categories import CategoryFactory


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'products.Product'

    name = factory.Faker('word')
    description = factory.Faker('sentence', nb_words=12)
    price = factory.LazyFunction(lambda: round(random.uniform(8.50, 25.00), 2))
    available = factory.Faker('boolean', chance_of_getting_true=80)
    category = factory.SubFactory(CategoryFactory)
    establishment = factory.SelfAttribute('category.establishment')
    # La imagen usará el default del modelo ('products/noproduct.png')
