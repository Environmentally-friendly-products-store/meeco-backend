from django.contrib.auth import get_user_model
from djoser.conf import settings
from djoser.serializers import UserSerializer
from rest_framework import serializers

from core.serializers import UserProductSerializer
from users.models import DeliveryAddress, Favorite, ShoppingCart

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


class CustomUserSerializer(UserSerializer):
    delivery_address = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            "phone",
            "delivery_address",
        )
        read_only_fields = (settings.LOGIN_FIELD,)

    def get_delivery_address(self, obj):
        if DeliveryAddress.objects.filter(user=obj).exists():
            return (
                DeliveryAddress.objects.filter(user=obj)
                .values(
                    "id",
                    "city",
                    "street",
                    "house",
                    "apartment",
                )
                .first()
            )
