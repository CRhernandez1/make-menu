import factory
from django.utils import timezone
from faker import Faker

from .data import LOCAL_NAMES
from .extras import UniqueFaker

TZ = timezone.get_current_timezone()
fake = Faker('es_ES')


class EstablishmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'establishments.Establishment'
        django_get_or_create = ('cif',)

    name = factory.Faker('random_element', elements=LOCAL_NAMES)
    legal_name = factory.LazyAttribute(lambda o: f'{o.name} S.L.')
    # Usamos UniqueFaker porque el modelo exige unique=True
    # 'bothify' crea una letra y 8 números (formato común de CIF)
    cif = UniqueFaker('bothify', text='?########')
    description = factory.Faker('paragraph', nb_sentences=3)
    zip_code = factory.Faker('postcode')
    city = factory.Faker('city')
    address = factory.Faker('address')
    # Limitamos a 16 caracteres como indica tu modelo
    phone = factory.Faker('numerify', text='###########')
    opened = factory.Faker('boolean', chance_of_getting_true=50)
