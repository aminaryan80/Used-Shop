from django.urls import path, include

from account import views
from account.models import CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('', views.index, name='home'),
    path('shop/', include('shop.urls')),
    path('register/', views.register, name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
