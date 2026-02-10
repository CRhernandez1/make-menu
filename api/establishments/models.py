from django.conf import settings
from django.db import models


class Establishment(models.Model):
    name = models.CharField()
    legal_name = models.CharField()
    cif = models.CharField(max_length=9, unique=True)
    description = models.TextField(blank=True)
    zip_code = models.CharField(max_length=10)
    city = models.CharField()
    address = models.TextField()
    phone = models.CharField(max_length=16)
    opened = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Table(models.Model):
    establishment = models.ForeignKey(
        'establishments.Establishment', related_name='tables', on_delete=models.CASCADE
    )
    max_guests = models.PositiveSmallIntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f' Mesa {self.pk}'


class Manage(models.Model):
    class Role(models.TextChoices):
        WAITER = 'waiter'
        MANAGER = 'manager'
        KITCHEN = 'kitchen'

    establishment = models.ForeignKey(
        'establishments.Establishment', related_name='manages', on_delete=models.PROTECT
    )
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='manages', on_delete=models.CASCADE
    )

    role = models.CharField(choices=Role)
    joined_at = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.member.first_name}: {self.role}'
