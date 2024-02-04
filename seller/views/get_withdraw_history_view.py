from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsSeller
from seller.models.seller import Seller
from seller.models.withdraw_history import WithdrawHistory
from shop.utils import handle_error


class GetWithdrawHistoryView(APIView):
    permission_classes = (IsSeller,)

    @handle_error
    def get(self, request, *args, **kwargs):
        seller_id = request.user.id
        seller = Seller.objects.get(user_id=seller_id)

        withdraw_history = WithdrawHistory.objects.order_by('-date').filter(seller=seller)

        return Response(
            [
                {
                    'amount': record.amount,
                    'date': record.date,
                }
                for record in withdraw_history
            ],
            status=status.HTTP_200_OK
        )
