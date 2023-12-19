from django.db import models
from django.utils import timezone

from account.models import Account


class Customer(Account):
    pass


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.JSONField(default=dict)


class DepositHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    date = models.DateField(default=timezone.now)
