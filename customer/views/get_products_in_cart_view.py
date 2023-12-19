from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsCustomer
from customer.models import Customer, Cart
from shop.utils import handle_error


class GetProductsInCart(APIView):
    permission_classes = (IsCustomer,)

    @handle_error
    def get(self, request, *args, **kwargs):
        customer_id = request.user.id
        customer = Customer.objects.get(user_id=customer_id)

        cart = Cart.objects.get(customer=customer)

        return Response(
            [
                {
                    'id': product['id'],
                    'count': product['count'],
                }
                for product in cart.products
            ],
            status=status.HTTP_200_OK
        )
