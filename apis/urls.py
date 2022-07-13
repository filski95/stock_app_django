from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import StockAPIView, UserAPIDetailView, UserAPIView

urlpatterns = [
    path("stocks/", StockAPIView.as_view(), name="stock_list"),
    path("users/", UserAPIView.as_view(), name="users_list"),
    path("users/<int:pk>/", UserAPIDetailView.as_view(), name="user_detail"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
