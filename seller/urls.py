from django.urls import path

from seller.views.get_sell_history_view import GetSellHistoryView
from seller.views.get_withdraw_history_view import GetWithdrawHistoryView
from seller.views.withdraw_view import WithdrawView

urlpatterns = [
    path('seller/withdraw/', WithdrawView.as_view(), name="withdraw"),
    path('seller/withdraw-history/', GetWithdrawHistoryView.as_view(), name="withdraw_history"),
    path('seller/sell-history/', GetSellHistoryView.as_view(), name="sell_history"),
]
