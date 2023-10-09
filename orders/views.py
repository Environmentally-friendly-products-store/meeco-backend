from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsOwnerOrReadOnly
from orders.models import Order, OrderProduct
from orders.serializers import OrderSerializer
from orders.services import Cart


class OrderAPIView(APIView):
    """
    API to handle order operations
    """

    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request):
        qs = Order.objects.filter(customer=request.user)
        serializer = OrderSerializer(qs, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        cart = Cart(request)
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = Order.objects.create(**serializer.data)
            for product, data in cart:
                OrderProduct.objects.create(
                    order_id=order.id,
                    product_id=product["id"],
                    amount=data["amount"],
                    purchase_price=data["price"],
                    item_total=data["total_price"],
                )
            cart.clear()
            # order_created.delay(order.id)
            self.request.session["order_id"] = order.id
        serializer.save(customer=self.request.user)

        return Response(
            {"message": "order created"},
            status=status.HTTP_201_CREATED,
        )


class CartListAPI(APIView):
    """
    Multi API to handle cart operations
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cart = Cart(request)

        if request.user.is_authenticated:
            if not cart:
                return Response(
                    {
                        "message": "no cart in session, please, "
                        "use ShoppingCart endpoint for DB cart"
                    },
                    status=status.HTTP_204_NO_CONTENT,
                )
            cart.build_cart(request.user)
            return Response(
                {"message": "cart uploaded to DB"},
                status=status.HTTP_201_CREATED,
            )

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

    permission_classes = [permissions.AllowAny]
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
