from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsSeller
from seller.models.sell_history import SellHistory
from seller.models.seller import Seller
from shop.utils import handle_error


class GetSellHistoryView(APIView):
    permission_classes = (IsSeller,)

    @handle_error
    def get(self, request, *args, **kwargs):
        seller_id = request.user.id
        seller = Seller.objects.get(user_id=seller_id)

        sell_history = SellHistory.objects.order_by('-date').filter(product__seller=seller)

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
                    'is_deleted': record.product.is_deleted,
                    'date': record.date,
                }
                for record in sell_history
            ],
            status=status.HTTP_200_OK
        )
