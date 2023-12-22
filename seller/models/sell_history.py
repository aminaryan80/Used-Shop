from django.db import models
from django.utils import timezone

from customer.models import Customer
from shop.models import SellingProduct


class SellHistory(models.Model):
    product = models.ForeignKey(SellingProduct, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    date = models.DateField(default=timezone.now)
