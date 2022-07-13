from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import StockAPIView, UserAPIDetailView, UserAPIView, api_root

app_name = "apis"
urlpatterns = [
    path("", api_root, name="main_api"),
    path("stocks/", StockAPIView.as_view(), name="stock_list"),
    path("users/", UserAPIView.as_view(), name="users_list"),
    path("users/<int:pk>/", UserAPIDetailView.as_view(), name="user_detail"),
]
urlpatterns = format_suffix_patterns(urlpatterns)  # urls can end with .json to only render serialized data
