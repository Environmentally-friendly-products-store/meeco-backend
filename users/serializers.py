from core.serializers import UserProductSerializer
from users.models import Favorite, ShoppingCart


class FavoriteSerializer(UserProductSerializer):
    class Meta(UserProductSerializer.Meta):
        model = Favorite


class ShoppingCartSerializer(UserProductSerializer):
    class Meta:
        model = ShoppingCart
        fields = ["user", "product", "amount"]
