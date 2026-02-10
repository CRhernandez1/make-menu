from django.db import models


class Order(models.Model):
    class Status(models.IntegerChoices):
        CANCELLED = -1
        INITIATED = 1
        IN_PROGRESS = 2
        DONE = 3

    status = models.SmallIntegerField(choices=Status, default=Status.INITIATED)
    table = models.ForeignKey(
        'establishments.Table', related_name='orders', on_delete=models.PROTECT
    )
    establishment = models.ForeignKey(
        'establishments.Establishment', related_name='orders', on_delete=models.CASCADE
    )
    placed_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    closed_at = models.DateTimeField()

    def __str__(self):
        return f'{self.pk}: {self.get_status_display()}'


class OrderDetail(models.Model):
    order = models.ForeignKey(
        'orders.Order', related_name='orders_details', on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        'products.product', related_name='orders_details', on_delete=models.PROTECT
    )

    price = models.DecimalField(max_digits=6, decimal_places=2)
    notes = models.TextField(blank=True)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.pk}: {self.price}'
