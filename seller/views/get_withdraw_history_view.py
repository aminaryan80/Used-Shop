from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsCustomer
from customer.models import Customer, DepositHistory
from shop.utils import handle_error


class GetDepositHistoryView(APIView):
    permission_classes = (IsCustomer,)

    @handle_error
    def get(self, request, *args, **kwargs):
        customer_id = request.user.id
        customer = Customer.objects.get(user_id=customer_id)

        deposit_history = DepositHistory.objects.order_by('-date').filter(customer=customer)

        return Response(
            [
                {
                    'amount': record.amount,
                    'date': record.date,
                }
                for record in deposit_history
            ],
            status=status.HTTP_200_OK
        )
