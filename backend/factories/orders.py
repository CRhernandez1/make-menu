import random

import factory
from django.utils import timezone
from factories.establishments import EstablishmentFactory
from factories.products import ProductFactory
from factories.tables import TableFactory
from faker import Faker
from orders.models import Order

fake = Faker('es_ES')


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'orders.Order'

    establishment = factory.SubFactory(EstablishmentFactory)
    table = factory.SubFactory(TableFactory)
    status = factory.Faker('random_element', elements=Order.Status.values)
    paid = factory.LazyAttribute(lambda o: o.status == Order.Status.DONE)
    total = 0.00

    @factory.lazy_attribute
    def closed_at(self):
        if self.status == Order.Status.DONE:
            return timezone.now()
        return None


class OrderDetailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'orders.OrderDetail'

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)

    quantity = factory.Faker('random_int', min=1, max=4)
    price = 0.00
    notes = factory.LazyAttribute(
        lambda o: fake.sentence(nb_words=4) if random.randint(1, 100) <= 20 else ''
    )
