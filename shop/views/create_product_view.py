from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsSeller
from shop.models import Product
from shop.utils import handle_error


class CreateProductView(APIView):
    permission_classes = (IsSeller,)

    @handle_error
    def post(self, request, *args, **kwargs):
        name = request.data.get('name', '')
        image = request.data.get('image', '')

        if not name or not image:
            return Response({'error': 'Name and image are required fields'}, status=status.HTTP_400_BAD_REQUEST)

        product = Product.objects.create(name=name, image=image)
        return Response({'id': product.id, 'name': product.name, 'image': product.image.url},
                        status=status.HTTP_201_CREATED)
