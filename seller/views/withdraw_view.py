from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsSeller
from seller.models.seller import Seller
from seller.models.withdraw_history import WithdrawHistory
from shop.utils import handle_error


class WithdrawView(APIView):
    permission_classes = (IsSeller,)

    @handle_error
    def post(self, request, *args, **kwargs):
        seller_id = request.user.id
        seller = Seller.objects.get(user_id=seller_id)
        amount = int(request.data.get('amount', 0))

        if amount > seller.balance:
            return Response(
                {
                    'username': seller.user.username,
                    'balance': seller.balance,
                }
                ,
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        seller.balance -= amount
        seller.save()

        WithdrawHistory.objects.create(seller=seller, amount=amount)

        return Response(
            {
                'username': seller.user.username,
                'balance': seller.balance,
            }
            ,
            status=status.HTTP_202_ACCEPTED
        )
