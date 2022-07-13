from accounts.models import CustomUser
from rest_framework import generics, serializers
from stocks_app.models import Stock


class StockSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=True)

    class Meta:
        model = Stock
        fields = ["name", "user"]


class UsersSerializer(serializers.ModelSerializer):
    stock = serializers.StringRelatedField(many=True)  # listing stocks in the user's api under "stock" field

    class Meta:
        model = CustomUser
        fields = "__all__"
