from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import SellingProduct
from shop.utils import handle_error


class GetFilteredSellingProductsView(APIView):
    permission_classes = ()

    @handle_error
    def get(self, request, *args, **kwargs):
        name_filter = request.data.get('name_filter', '')

        selling_products = SellingProduct.objects.filter(is_deleted=False)

        if name_filter != '':
            selling_products = selling_products.filter(product__name__contains=name_filter)

        response = [
            {
                'id': selling_product.id,
                'name': selling_product.product.name,
                'image': selling_product.product.image.url,
                'color': selling_product.color_variant.color,
                'size': selling_product.size_variant.size,
                'properties': selling_product.properties_variant.properties,
                'price': selling_product.price,
                'stock_count': selling_product.stock_count
            }
            for selling_product in selling_products
        ]

        return Response(response, status=status.HTTP_202_ACCEPTED)
