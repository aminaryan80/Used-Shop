from django.urls import path

from seller.views.get_sell_history_view import GetSellHistoryView

urlpatterns = [
    path('customer/deposit/', DepositView.as_view(), name="withdraw"),
    path('customer/deposit-history/', GetDepositHistoryView.as_view(), name="withdraw_history"),
    path('seller/sell-history/', GetSellHistoryView.as_view(), name="sell_history"),
]
