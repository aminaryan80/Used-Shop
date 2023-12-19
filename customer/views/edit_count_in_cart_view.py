from typing import Dict, List

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsCustomer
from customer.models import Customer, Cart
from shop.models import SellingProduct
from shop.utils import handle_error


class EditCountInCartView(APIView):
    permission_classes = (IsCustomer,)

    @handle_error
    def put(self, request, *args, **kwargs):
        selling_product_id = request.data.get('selling_product_id', '')
        count = request.data.get('count', '')
        customer_id = request.user.id
        customer = Customer.objects.get(user_id=customer_id)

        if not selling_product_id:
            return Response({'error': 'selling_product_id is required fields'}, status=status.HTTP_400_BAD_REQUEST)
        elif not count:
            return Response({'error': 'count is required fields'}, status=status.HTTP_400_BAD_REQUEST)

        count = int(count)

        selling_product = SellingProduct.objects.get(id=selling_product_id)

        cart = Cart.objects.get(customer=customer)

        cart_products: List[Dict] = cart.products

        for product in cart_products:
            if product['id'] == selling_product_id:
                if selling_product.stock_count + product['count'] < count:
                    return Response({'error': 'not enough stock'}, status=status.HTTP_400_BAD_REQUEST)

                product['count'] = count
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
            status=status.HTTP_202_ACCEPTED
        )
