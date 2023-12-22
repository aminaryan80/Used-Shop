from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import PriceHistory
from shop.utils import handle_error


class GetPriceHistoryView(APIView):
    permission_classes = ()

    @handle_error
    def get(self, request, selling_product_id, *args, **kwargs):
        price_history = PriceHistory.objects.filter(selling_product_id=selling_product_id)

        return Response(
            [
                {
                    'price': record.price,
                    'date': record.date,
                }
                for record in price_history
            ],
            status=status.HTTP_200_OK
        )
