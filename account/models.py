from django.contrib.auth.models import User
from django.db import models
from django.http import HttpResponse
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

SELLER = "SELLER"
CUSTOMER = "CUSTOMER"

USER_TYPE_CHOICES = ((SELLER, "Seller"), (CUSTOMER, "Customer"), ("ADMIN", "Admin"))


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=20)
    user_type = models.CharField(max_length=8, choices=USER_TYPE_CHOICES)
    balance = models.PositiveIntegerField()


class CustomTokenObtainPairView(TokenObtainPairView):
    def get(self, request):
        return HttpResponse("Method `GET` is not allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CustomTokenRefreshView(TokenRefreshView):
    def get(self, request):
        return HttpResponse("Method `GET` is not allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)
