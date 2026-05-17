import factory
from django.contrib.auth.models import User
from establishments.models import Manage
from factories.establishments import EstablishmentFactory
from users.models import Member, Token

factory.Faker._DEFAULT_LOCALE = 'es_ES'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', '1234')


class MemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Member

    user = factory.SubFactory(UserFactory)
    phone = factory.Faker('phone_number')


class TokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Token

    user = factory.SubFactory(UserFactory)


class ManageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Manage

    establishment = factory.SubFactory(EstablishmentFactory)
    member = factory.SubFactory(UserFactory)
    role = factory.Faker('random_element', elements=Manage.Role.values)
