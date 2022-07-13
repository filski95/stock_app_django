from accounts.models import CustomUser
from rest_framework import generics, permissions
from rest_framework.response import Response
from stocks_app.models import Stock

from .serializers import StockSerializer, UsersSerializer


class StockAPIView(generics.ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class UserAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer


class UserAPIDetailView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer
