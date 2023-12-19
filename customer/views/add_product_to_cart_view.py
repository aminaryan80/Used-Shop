from typing import Dict, List

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsCustomer
from customer.models import Customer, Cart
from shop.models import SellingProduct
from shop.utils import handle_error


class AddProductToCartView(APIView):
    permission_classes = (IsCustomer,)

    @handle_error
    def put(self, request, *args, **kwargs):
        selling_product_id = request.data.get('selling_product_id', '')
        count = request.data.get('count', '')
        customer_id = request.user.id
        customer = Customer.objects.get(user_id=customer_id)

        selling_product = SellingProduct.objects.get(id=selling_product_id)
        count = int(count)

        if selling_product.is_deleted:
            return Response({'error': 'selling_product is deleted'}, status=status.HTTP_404_NOT_FOUND)

        if not selling_product_id:
            return Response({'error': 'selling_product_id is required fields'}, status=status.HTTP_400_BAD_REQUEST)
        elif not count:
            return Response({'error': 'count is required fields'}, status=status.HTTP_400_BAD_REQUEST)

        if selling_product.stock_count < count:
            return Response({'error': 'not enough stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart.objects.get(customer=customer)
        cart_products: List[Dict] = cart.products
        if selling_product_id in [p['id'] for p in cart_products]:
            return Response({'error': 'product already added to cart'}, status=status.HTTP_400_BAD_REQUEST)

        cart_products.append({'id': selling_product_id, 'count': count})
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
