from django.urls import path

from shop.views.create_product_view import CreateProductView
from shop.views.create_selling_product_view import CreateSellingProductView
from shop.views.edit_selling_product_view import EditSellingProductView
from shop.views.get_filtered_selling_products_view import GetFilteredSellingProductsView
from shop.views.get_selling_product_view import GetSellingProductView
from shop.views.get_price_history_view import GetPriceHistoryView

urlpatterns = [
    path('product/create/', CreateProductView.as_view(), name="create_product"),
     path('product/<int:product_id>/', CreateProductView.as_view(), name="get_product_view"),
    path('selling-product/create/', CreateSellingProductView.as_view(), name="create_selling_product"),
    path('selling-product/<int:selling_product_id>/update/', EditSellingProductView.as_view(), name="edit_selling_product"),
    path('selling-product/<int:selling_product_id>/', GetSellingProductView.as_view(), name="get_selling_product"),
    path('selling-product/<int:selling_product_id>/price-history', GetPriceHistoryView.as_view(), name="get_price_history"),
    path('selling-product/filter/', GetFilteredSellingProductsView.as_view(), name="get_filtered_selling_products"),
]
