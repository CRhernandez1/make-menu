import factory
from django.contrib.auth.models import User

from establishments.models import Manage
from factories.establishments import EstablishmentFactory
from users.models import Member, Token

# Configuración global para que todos los datos sean en español de España
factory.Faker._DEFAULT_LOCALE = 'es_ES'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')

    # Contraseña fija y encriptada
    password = factory.PostGenerationMethodCall('set_password', '1234')


class MemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Member

    user = factory.SubFactory(UserFactory)
    phone = factory.Faker('phone_number')
    # avatar usa el default


class TokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Token

    user = factory.SubFactory(UserFactory)
    # key se genera solo con uuid4


class ManageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Manage

    establishment = factory.SubFactory(EstablishmentFactory)

    # OJO: En tu modelo, el campo 'member' apunta a User (AUTH_USER_MODEL)
    member = factory.SubFactory(UserFactory)

    role = factory.Faker('random_element', elements=Manage.Role.values)
    # joined_at se pone solo con auto_now_add
