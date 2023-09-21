from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from core.views import UserProductViewSet
from products.models import Product
from users.models import ShoppingCart
from users.serializers import ShoppingCartSerializer

User = get_user_model()


class UserRegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer) -> None:
        if "username" in self.request.data:
            username = self.request.data["username"]
        else:
            username = "NoUserName"
        serializer.save(username=username)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request, *args, **kwargs):
    user = get_object_or_404(User, pk=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data)


# class FavoriteView(UserProductViewSet):
#     queryset = Favorite.objects.all()
#     serializer = FavoriteSerializer
#     message = 'избранное'
#     message_plural = 'избранном'
#     name = "favorite"


class ShoppingCartViewSet(UserProductViewSet):
    queryset = ShoppingCart.objects.all()
    serializer = ShoppingCartSerializer
    message = "список покупок"
    message_plural = "списке покупок"
    name = "shopping_card"

    @action(
        methods=["patch"],
        detail=True,
    )
    def patch(self, request: Request, product_id: int) -> Response:
        user_id = request.user.id
        product = get_object_or_404(Product, pk=product_id)
        if not self.queryset.filter(user=user_id, product=product).exists():
            return Response(
                {"Ошибка": f"Товара нет в {self.message_plural}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        amount = request.data.get("amount")
        if amount < 1:
            return Response(
                {"Ошибка": "Количество для изменения не может быть меньше 1"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ShoppingCart.objects.filter(user=request.user.id, product=product_id).update(
            amount=amount
        )
        return self.get_return_page(product_id, amount)
