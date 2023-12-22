from django.db import models
from django.utils import timezone


class WithdrawHistory(models.Model):
    amount = models.PositiveIntegerField()
    date = models.DateField(default=timezone.now)
