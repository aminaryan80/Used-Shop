from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import Product
from shop.utils import handle_error


class GetFilteredProductsView(APIView):
    permission_classes = ()

    @handle_error
    def get(self, request, *args, **kwargs):
        name_filter = request.data.get('name_filter', '')

        products = Product.objects.all()

        if name_filter != '':
            products = products.filter(product__name__contains=name_filter)

        response = [
            {
                'id': product.id,
                'name': product.name,
                'image': product.image.url,
            }
            for product in products
        ]

        return Response(response, status=status.HTTP_200_OK)
