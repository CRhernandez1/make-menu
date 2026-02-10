from django.db import models


class Product(models.Model):
    class Category(models.TextChoices):
        DRINKS = 'drinks'
        DESSERTS = 'desserts'
        FOOD = 'food'

    establishment = models.ForeignKey(
        'establishments.Establishment', related_name='products', on_delete=models.CASCADE
    )
    category = models.CharField(choices=Category)
    name = models.CharField()
    description = models.TextField(blank=True)
    product_image = models.ImageField(upload_to='products', default='products/noproduct.png')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    establishment = models.ForeignKey(
        'establishments.Establishment', related_name='ingredients', on_delete=models.CASCADE
    )
    name = models.CharField()
    description = models.TextField(blank=True)
    # en un futuro: allergens = models.CharField(blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Component(models.Model):
    class Unity(models.TextChoices):
        UNITY = 'ud'
        GRAMS = 'gr'
        KILOGRAMS = 'kg'
        LITERS = 'l'
        MILILITERS = 'ml'
        CENTILITERS = 'cl'

    product = models.ForeignKey(
        'products.product', related_name='components', on_delete=models.PROTECT
    )
    ingredient = models.ForeignKey(
        'products.ingredient', related_name='components', on_delete=models.PROTECT
    )
    quantity = models.PositiveSmallIntegerField()
    unity = models.CharField(choices=Unity, max_length=2)
