from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.serializers import UserProductSerializer
from users.models import Favorite, ShoppingCart

User = get_user_model()


class PasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["new_password", "current_password"]


class FavoriteSerializer(UserProductSerializer):
    class Meta(UserProductSerializer.Meta):
        model = Favorite


class ShoppingCartSerializer(UserProductSerializer):
    class Meta:
        model = ShoppingCart
        fields = ["user", "product", "amount"]
