from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsSeller
from shop.models import Product
from shop.utils import handle_error

class GetProductView(APIView):
    permission_classes = (IsSeller,)

    @handle_error
    def get(self, request, product_id, *args, **kwargs):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        response_data = {
            'id': product.id,
            'name': product.name,
            'image': product.image.url,
            # Add more fields as needed
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
