from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsCustomer
from customer.models import Customer
from seller.models.sell_history import SellHistory
from shop.utils import handle_error


class GetBuyHistoryView(APIView):
    permission_classes = (IsCustomer,)

    @handle_error
    def get(self, request, *args, **kwargs):
        customer_id = request.user.id
        customer = Customer.objects.get(user_id=customer_id)

        buy_history = SellHistory.objects.order_by('-date').filter(customer=customer)

        return Response(
            [
                {
                    'id': record.product.id,
                    'name': record.product.product.name,
                    'image': record.product.product.image.url,
                    'color': record.product.color_variant.color,
                    'size': record.product.size_variant.size,
                    'properties': record.product.properties_variant.properties,
                    'price': record.total_price,
                    'count': record.count,
                    'date': record.date,
                }
                for record in buy_history
            ],
            status=status.HTTP_200_OK
        )
