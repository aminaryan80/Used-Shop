from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsSeller
from seller.models.seller import Seller
from shop.models import SellingProduct, COLOR_CHOICES
from shop.utils import handle_error


def _clean_color(color):
    for code, name in COLOR_CHOICES:
        if color == name:
            return code

    raise LookupError('Color invalid')


class DeleteSellingProductView(APIView):
    permission_classes = (IsSeller,)

    @handle_error
    def delete(self, request, selling_product_id, *args, **kwargs):
        seller_id = request.user.id
        seller = Seller.objects.get(user_id=seller_id)

        selling_product = SellingProduct.objects.get(id=selling_product_id)
        if selling_product.seller.id != seller.id:
            return Response({'error': 'not enough balance'}, status=status.HTTP_401_UNAUTHORIZED)

        selling_product.is_deleted = 1
        selling_product.save()

        return Response('', status=status.HTTP_204_NO_CONTENT)
