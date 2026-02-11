from django.core.management.base import BaseCommand
from django.db import transaction

from establishments.models import Establishment
from factories.establishment import EstablishmentFactory


class Command(BaseCommand):
    help = 'Genera establecimientos de prueba'

    def add_arguments(self, parser):
        # Añadimos la opción --delete
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Borra todos los establecimientos antes de crear los nuevos',
        )

    def handle(self, *args, **options):
        if options['delete']:
            count = Establishment.objects.count()
            Establishment.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'🗑️ Borrados {count} establecimientos viejos.'))

        self.stdout.write(self.style.SUCCESS('🚀 Creando 20 nuevos establecimientos...'))

        with transaction.atomic():
            EstablishmentFactory.create_batch(20)

            self.stdout.write(self.style.SUCCESS('✨ ¡Listo!'))
