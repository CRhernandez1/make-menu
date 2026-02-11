from django.db import models


class Category(models.Model):
    establishment = models.ForeignKey(
        'establishments.Establishment', related_name='categories', on_delete=models.CASCADE
    )
    name = models.CharField()

    def __str__(self):
        return f'{self.name} ({self.establishment.name})'


class Product(models.Model):
    establishment = models.ForeignKey(
        'establishments.Establishment', related_name='products', on_delete=models.CASCADE
    )
    category = models.ForeignKey(Category, related_name='products', on_delete=models.PROTECT)
    name = models.CharField()
    description = models.TextField(blank=True)
    product_image = models.ImageField(upload_to='products', default='products/noproduct.png')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    class Type(models.TextChoices):
        MEAT = 'meat'
        FISH = 'fish'
        VEGETABLES = 'vegetables'
        DAIRY = 'dairy'
        BAKERY = 'bakery'
        SAUCES = 'sauces'
        DRINKS = 'drinks'
        OTHER = 'other'

    establishment = models.ForeignKey(
        'establishments.Establishment', related_name='ingredients', on_delete=models.CASCADE
    )
    allergens = models.ManyToManyField(
        'products.Allergen',
        blank=True,
        related_name='ingredients',
    )
    ingredient_type = models.CharField(choices=Type.choices, default=Type.OTHER)
    name = models.CharField()
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Component(models.Model):
    class Unity(models.TextChoices):
        UNITY = 'ud', 'Unidades'
        GRAMS = 'gr', 'Gramos'
        KILOGRAMS = 'kg', 'Kilos'
        LITERS = 'l', 'Litros'
        MILILITERS = 'ml', 'Mililitros'

    product = models.ForeignKey(
        'products.product', related_name='components', on_delete=models.PROTECT
    )
    ingredient = models.ForeignKey(
        'products.ingredient', related_name='components', on_delete=models.PROTECT
    )
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unity = models.CharField(choices=Unity.choices, max_length=2)
    removable = models.BooleanField(default=True)


class Allergen(models.Model):
    name = models.CharField(unique=True)
    icon = models.ImageField(
        upload_to='allergens/', default='allergens/noallergen.png', blank=True, null=True
    )

    def __str__(self):
        return self.name
