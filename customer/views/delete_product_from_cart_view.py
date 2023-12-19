from typing import Dict, List

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsCustomer
from customer.models import Customer, Cart
from shop.utils import handle_error


class DeleteProductFromCartView(APIView):
    permission_classes = (IsCustomer,)

    @handle_error
    def delete(self, request, *args, **kwargs):
        selling_product_id = request.data.get('selling_product_id', '')
        customer_id = request.user.id
        customer = Customer.objects.get(user_id=customer_id)

        if not selling_product_id:
            return Response({'error': 'selling_product_id is required fields'}, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart.objects.get(customer=customer)

        cart_products: List[Dict] = cart.products

        for product in cart_products:
            if product['id'] == selling_product_id:
                cart_products.remove(product)
                break

        cart.products = cart_products

        cart.save()

        return Response(
            [
                {
                    'id': product['id'],
                    'count': product['count'],
                }
                for product in cart.products
            ],
            status=status.HTTP_204_NO_CONTENT
        )
