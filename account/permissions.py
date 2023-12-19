from rest_framework.permissions import IsAuthenticated

from customer.models import Customer
from seller.models.seller import Seller


class IsSeller(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        return Seller.objects.filter(user=request.user).count() == 1


class IsCustomer(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        return Customer.objects.filter(user=request.user).count() == 1
