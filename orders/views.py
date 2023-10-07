from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from api.pagination import Pagination
from api.permissions import IsOwnerOrReadOnly
from orders.models import Order
from orders.serializers import OrderListSerializer, OrderSerializer
from orders.services import Cart


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("customer").all()
    pagination_class = Pagination
    permission_classes_by_action = {
        "current_user_orders": [IsOwnerOrReadOnly],
        "list": [permissions.IsAdminUser],
        "retrieve": [IsOwnerOrReadOnly],
        "create": [permissions.IsAuthenticatedOrReadOnly],
    }

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return OrderSerializer

    @action(detail=False, url_path="my")
    def current_user_orders(self, request):
        queryset = self.get_queryset().filter(customer=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    # def perform_update(self, serializer):
    #     serializer.save(customer=self.request.user)

    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class CartListAPI(APIView):
    """
    Multi API to handle cart operations
    """

    def get(self, request):
        cart = Cart(request)

        return Response(
            {
                "data": list(cart.__iter__()),
                "cart_total_price": cart.get_total_price(),
                # "DEBUG": f"{request.user}, s-key: {cart.session.session_key}"
                # "DEBUG": f"{request.session.items()}",
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        cart = Cart(request)
        if "amount" not in request.data.keys():
            cart.add(product_id=request.data["product"])
        else:
            cart.add(
                product_id=request.data["product"],
                amount=request.data["amount"],
            )

        return Response(
            {"message": "cart is updated"},
            status=status.HTTP_202_ACCEPTED,
        )

    def delete(self, request):
        cart = Cart(request)
        cart.clear()

        return Response(
            {"message": "cart  is cleared"},
            status=status.HTTP_204_NO_CONTENT,
        )


class CartDetailAPI(APIView):
    """
    Single API to handle cart operations
    """

    message = "cart details updated"

    def patch(self, request, **kwargs):
        cart = Cart(request)
        cart.add(
            product_id=kwargs["pk"],
            amount=request.data["amount"],
            overide_amount=True,
        )

        return Response(
            {"message": self.message},
            status=status.HTTP_205_RESET_CONTENT,
        )

    def delete(self, request, **kwargs):
        cart = Cart(request)
        cart.remove(kwargs["pk"])

        return Response(
            {"message": self.message},
            status=status.HTTP_204_NO_CONTENT,
        )
