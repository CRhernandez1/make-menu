import factory
from django.utils import timezone

from .data import LOCAL_NAMES
from .extras import UniqueFaker

factory.Faker._DEFAULT_LOCALE = 'es_ES'
TZ = timezone.get_current_timezone()


class EstablishmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'establishments.Establishment'
        django_get_or_create = ('cif',)

    name = factory.Faker('random_element', elements=LOCAL_NAMES)
    legal_name = factory.LazyAttribute(lambda o: f'{o.name} S.L.')
    # 'bothify' crea una letra y 8 números (formato común de CIF)
    cif = UniqueFaker('bothify', text='?########')
    description = factory.Faker('paragraph', nb_sentences=3)
    zip_code = factory.Faker('postcode')
    city = factory.Faker('city')
    address = factory.Faker('address')
    phone = factory.Faker('numerify', text='###########')
    opened = factory.Faker('boolean', chance_of_getting_true=50)
