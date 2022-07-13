from accounts.models import CustomUser
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
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


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("apis:users_list", request=request, format=format),
            "stocks": reverse("apis:stock_list", request=request, format=format),
        }
    )
