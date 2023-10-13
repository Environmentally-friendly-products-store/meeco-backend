from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsOwnerOrReadOnly
from orders import appvars as VARS
from orders.models import Order
from orders.serializers import OrderSerializer
from orders.services.cart import Cart
from orders.services.orders import build_order
from users.models import ShoppingCart


class OrderAPIView(APIView):
    """
    API to handle order operations
    """

    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request):
        qs = Order.objects.filter(customer=request.user)
        serializer = OrderSerializer(qs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        db_cart = ShoppingCart.objects.filter(user=request.user.id)
        if not db_cart:
            return Response(
                {"message": "no data in DB cart"},
                status=status.HTTP_204_NO_CONTENT,
            )
        serializer = OrderSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(customer=self.request.user)
            order_id = serializer.data["id"]
            build_order(db_cart, order_id)
            # order_created.delay(order.id)
            self.request.session[VARS.ORDER_SESSION_ID] = order_id
            new_order = OrderSerializer(Order.objects.get(id=order_id))
            return Response(new_order.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartListAPI(APIView):
    """
    Multi API to handle cart operations
    """

    permission_classes = [~permissions.IsAuthenticated]

    def get(self, request):
        cart = Cart(request)

        # Эта часть кода работает только, когда  есть permission
        # if request.user.is_authenticated:
        #     if not cart:
        #         return Response(
        #             {
        #                 "message": "no cart in session, please, "
        #                 "use ShoppingCart endpoint for DB cart"
        #             },
        #             status=status.HTTP_204_NO_CONTENT,
        #         )
        #     cart.build_cart(request.user)
        #     return Response(
        #         {"message": "cart uploaded to DB"},
        #         status=status.HTTP_201_CREATED,
        #     )

        return Response(
            {
                "data": list(cart.__iter__()),
                "cart_total_price": cart.get_total_price(),
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

    permission_classes = [~permissions.IsAuthenticated]
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
