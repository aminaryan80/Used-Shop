from django.db import models
from django.utils import timezone

from seller.models.seller import Seller


class WithdrawHistory(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    date = models.DateField(default=timezone.now)
