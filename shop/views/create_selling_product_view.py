from typing import Dict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsSeller
from seller.models.seller import Seller
from shop.models import Product, SellingProduct, PropertiesVariant, ColorVariant, SizeVariant, COLOR_CHOICES
from shop.utils import handle_error


def _clean_color(color):
    for code, name in COLOR_CHOICES:
        if color == name:
            return code

    raise LookupError('Color invalid')


class CreateSellingProductView(APIView):
    permission_classes = (IsSeller,)

    @handle_error
    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id', '')
        seller_id = request.user.id
        properties: Dict = request.data.get('properties', '')
        color = request.data.get('color', 'TRS')
        size = request.data.get('size', '')
        price = request.data.get('price', '')
        stock_count = request.data.get('stock_count', 0)

        if not product_id:
            return Response({'error': 'product_id are required fields'}, status=status.HTTP_400_BAD_REQUEST)
        elif not price:
            return Response({'error': 'price are required fields'}, status=status.HTTP_400_BAD_REQUEST)

        product = Product.objects.get(id=product_id)

        color = _clean_color(color)

        selling_product = SellingProduct.objects.create(
            product=Product.objects.get(id=product_id),
            seller=Seller.objects.get(user_id=seller_id),
            stock_count=stock_count,
            price=price,
            properties_variant=PropertiesVariant.objects.create(product=product, properties=properties),
            color_variant=ColorVariant.objects.create(product=product, color=color),
            size_variant=SizeVariant.objects.create(product=product, size=size)
        )

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
            status=status.HTTP_201_CREATED
        )
