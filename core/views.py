from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product
from users.models import Favorite, ShoppingCart

User = get_user_model()


class UserProductViewSet(APIView):
    queryset = None
    serializer = None
    message: str = ""
    message_plural: str = ""
    name: str = ""

    @action(
        methods=["post"],
        detail=True,
    )
    def post(self, request: Request, product_id: int) -> Response:
        user_id = request.user.id
        if self.queryset.filter(user=user_id, product=product_id).exists():
            return Response(
                {"error": f"Ошибка добавления в {self.message}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.serializer(data=self._get_data_to_save(user_id, product_id))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self._get_return_page(user_id, product_id)

    @action(
        methods=["delete"],
        detail=True,
    )
    def delete(self, request: Request, product_id: int) -> Response:
        user_id = request.user.id
        product = get_object_or_404(Product, pk=product_id)
        if not self.queryset.filter(user=user_id, product=product).exists():
            return Response(
                {"error": f"Товара нет в {self.message_plural}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.queryset.get(user=user_id, product=product).delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

    def _get_return_page(
        self, user_id: int, product_id: int, amount: int = 1
    ) -> Response:
        return_page = (
            Product.objects.filter(pk=product_id)
            .values(
                "id",
            )
            .first()
        )
        match self.name:
            case "favorite":
                return_page.update(
                    is_favorite=Favorite.objects.filter(
                        user=user_id, product=product_id
                    ).exists(),
                )
            case "shopping_card":
                return_page.update(
                    amount=amount,
                    is_in_shopping_cart=ShoppingCart.objects.filter(
                        user=user_id, product=product_id
                    ).exists(),
                )
        return Response(return_page, status=status.HTTP_201_CREATED)

    def _get_data_to_save(self, user_id: int, product_id: int) -> dict[str, int]:
        match self.name:
            case "favorite":
                return {"user": user_id, "product": product_id}
            case "shopping_card":
                return {
                    "user": user_id,
                    "product": product_id,
                    "amount": 1,
                }
        return {}
