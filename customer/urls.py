from django.urls import path

from customer.views.add_product_to_cart_view import AddProductToCartView
from customer.views.buy_products_in_cart_view import BuyProductsInCart
from customer.views.delete_product_from_cart_view import DeleteProductFromCartView
from customer.views.deposit_view import DepositView
from customer.views.edit_count_in_cart_view import EditCountInCartView
from customer.views.get_buy_history_view import GetBuyHistoryView
from customer.views.get_deposit_history_view import GetDepositHistoryView
from customer.views.get_products_in_cart_view import GetProductsInCart

urlpatterns = [
    path('cart/add/', AddProductToCartView.as_view(), name="add_selling_product_to_cart"),
    path('cart/delete/', DeleteProductFromCartView.as_view(), name="delete_selling_product_from_cart"),
    path('cart/edit/', EditCountInCartView.as_view(), name="edit_count_in_cart"),
    path('cart/buy/', BuyProductsInCart.as_view(), name="buy_products_in_cart"),
    path('cart/', GetProductsInCart.as_view(), name="get_cart"),
    path('customer/deposit/', DepositView.as_view(), name="deposit"),
    path('customer/deposit-history/', GetDepositHistoryView.as_view(), name="deposit_history"),
    path('customer/buy-history/', GetBuyHistoryView.as_view(), name="buy_history"),
]
