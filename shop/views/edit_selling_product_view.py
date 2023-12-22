from typing import Dict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsSeller
from shop.models import SellingProduct
from shop.utils import handle_error, are_dicts_equal
from shop.views.create_selling_product_view import _clean_color


class EditSellingProductView(APIView):
    permission_classes = (IsSeller,)

    @handle_error
    def put(self, request, selling_product_id, *args, **kwargs):
        properties: Dict = request.data.get('properties', '')
        color = request.data.get('color', '')
        size = request.data.get('size', '')
        price = request.data.get('price', '')
        stock_count = request.data.get('stock_count', 0)

        selling_product = SellingProduct.objects.get(id=selling_product_id)

        if selling_product.is_deleted:
            return Response({'error': 'selling_product is deleted'}, status=status.HTTP_404_NOT_FOUND)

        if not selling_product_id:
            return Response({'error': 'selling_product_id are required fields'}, status=status.HTTP_400_BAD_REQUEST)
        elif not price:
            return Response({'error': 'price are required fields'}, status=status.HTTP_400_BAD_REQUEST)

        color = _clean_color(color)

        if color != selling_product.color_variant.color:
            selling_product.color_variant.color = color
            selling_product.color_variant.save()

        if size != selling_product.size_variant.size:
            selling_product.size_variant.size = size
            selling_product.size_variant.save()

        if not are_dicts_equal(properties, selling_product.properties_variant.properties):
            selling_product.properties_variant.properties = properties
            selling_product.properties_variant.save()

        if stock_count != selling_product.stock_count:
            selling_product.stock_count = stock_count

        if price != selling_product.price:
            selling_product.price = price

        selling_product.save()

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
