from django.db import models
from django.utils import timezone

from seller.models.seller import Seller

COLOR_CHOICES = [
    ('RED', 'Red'),
    ('GRN', 'Green'),
    ('BLU', 'Blue'),
    ('YLW', 'Yellow'),
    ('BLK', 'Black'),
    ('WHT', 'White'),
    ('GRY', 'Gray'),
    ('ORG', 'Orange'),
]


class Product(models.Model):
    name = models.CharField(max_length=128, null=False)
    image = models.ImageField(upload_to='product_images/')


class ColorVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=3, choices=COLOR_CHOICES)


class SizeVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=20)


class PropertiesVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    properties = models.JSONField(default=dict)


class SellingProduct(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.DO_NOTHING)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.DO_NOTHING)
    properties_variant = models.ForeignKey(PropertiesVariant, on_delete=models.DO_NOTHING)
    price = models.PositiveIntegerField()
    stock_count = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    @property
    def is_available(self):
        return self.stock_count > 0

    def save(self, *args, **kwargs):
        old_price = SellingProduct.objects.get(pk=self.pk).price if self.pk is not None else -1

        super().save(*args, **kwargs)

        if self.price != old_price:
            PriceHistory.objects.create(selling_product=self, price=self.price)


class PriceHistory(models.Model):
    selling_product = models.ForeignKey(SellingProduct, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    date = models.DateField(default=timezone.now)
