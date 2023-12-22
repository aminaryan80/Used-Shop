from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import SellingProduct
from shop.utils import handle_error


class GetSellingProductView(APIView):
    permission_classes = ()

    @handle_error
    def get(self, request, selling_product_id, *args, **kwargs):
        selling_product = SellingProduct.objects.get(id=selling_product_id)

        if selling_product.is_deleted:
            return Response({'error': 'selling_product is deleted'}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {
                'id': selling_product.id,
                'name': selling_product.product.name,
                'image': selling_product.product.image.url,
                'color': selling_product.color_variant.color,
                'size': selling_product.size_variant.size,
                'properties': selling_product.properties_variant.properties,
                'price': selling_product.price,
                'stock_count': selling_product.stock_count
            },
            status=status.HTTP_202_ACCEPTED
        )
