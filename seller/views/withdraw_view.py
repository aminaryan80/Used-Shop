from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsCustomer
from customer.models import Customer, DepositHistory
from shop.utils import handle_error


class DepositView(APIView):
    permission_classes = (IsCustomer,)

    @handle_error
    def post(self, request, *args, **kwargs):
        customer_id = request.user.id
        customer = Customer.objects.get(user_id=customer_id)
        amount = int(request.data.get('amount', 0))

        customer.balance += amount
        customer.save()

        DepositHistory.objects.create(customer=customer, amount=amount)

        return Response(
            {
                'username': customer.user.username,
                'balance': customer.balance,
            }
            ,
            status=status.HTTP_202_ACCEPTED
        )
