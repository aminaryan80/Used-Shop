from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsCustomer
from customer.models import Customer, Cart
from seller.models.sell_history import SellHistory
from shop.models import SellingProduct
from shop.utils import handle_error


def _get_products_total_price(cart):
    total_price = 0

    selling_products = SellingProduct.objects.filter(id__in=[p['id'] for p in cart.products])

    selling_products_dict = dict()
    for selling_product in selling_products:
        selling_products_dict[selling_product.id] = selling_product

    merged_list = [
        {'id': item1['id'], 'count': item1['count'], 'price': item2['price']}
        for item1 in cart.products
        for item2 in selling_products.values('id', 'price')
        if int(item1['id']) == item2['id']
    ]

    for product in merged_list:
        total_price += product['price'] * product['count']
        product['product'] = selling_products_dict[int(product['id'])]

    return merged_list, total_price


class BuyProductsInCart(APIView):
    permission_classes = (IsCustomer,)

    @handle_error
    def post(self, request, *args, **kwargs):
        customer_id = request.user.id
        customer = Customer.objects.get(user_id=customer_id)

        cart = Cart.objects.get(customer=customer)

        selling_products_dict, total_price = _get_products_total_price(cart)

        if customer.balance < total_price:
            return Response({'error': 'not enough balance'}, status=status.HTTP_400_BAD_REQUEST)

        for selling_product in selling_products_dict:
            if selling_product['product'].is_deleted:
                return Response(
                    {
                        'error': f'selling_product {selling_product["id"]} is deleted',
                        'product_id': selling_product['id']
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

        for selling_product in selling_products_dict:
            SellHistory.objects.create(
                product=selling_product['product'],
                customer=customer,
                total_price=selling_product['price'] * selling_product['count'],
                count=selling_product['count']
            )

        customer.balance -= total_price
        customer.save()

        cart.products = dict()
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
