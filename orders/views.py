from rest_framework import permissions, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsOwnerOrReadOnly
from orders import appvars as VARS
from orders.models import Order
from orders.serializers import OrderSerializer
from orders.services.cart import Cart
from orders.services.dbcart import DBCart


class OrderAPIView(APIView, LimitOffsetPagination):
    """
    API to handle order operations
    """

    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request):
        qs = Order.objects.filter(customer=request.user)
        paginated_qs = self.paginate_queryset(qs, request, view=self)
        serializer = OrderSerializer(paginated_qs, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        dbcart = DBCart(request)
        if not dbcart:
            return Response(
                {"message": "no data in DB cart"},
                status=status.HTTP_204_NO_CONTENT,
            )
        serializer = OrderSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(customer=self.request.user)
            order_id = serializer.data["id"]

            # order_created.delay(order_id)
            self.request.session[VARS.ORDER_SESSION_ID] = order_id

            order_instance = Order.objects.get(id=order_id)
            order_instance.price_total = dbcart.build_order(order_instance)
            order_instance.save()
            new_order = OrderSerializer(order_instance)
            return Response(new_order.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartListAPI(APIView):
    """
    Multi API to handle cart operations
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        if not request.user.is_anonymous:
            dbcart = DBCart(request)
            return Response(
                {
                    "items_count": dbcart.__len__(),
                    "cart_total_price": dbcart.get_total_price(),
                    "data": list(dbcart.__iter__()),
                },
                status=status.HTTP_200_OK,
            )

        cart = Cart(request)
        return Response(
            {
                "items_count": cart.__len__(),
                "cart_total_price": cart.get_total_price(),
                "data": list(cart.__iter__()),
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        if not request.user.is_anonymous:
            dbcart = DBCart(request)
            data = {
                "product_id": request.data["product"],
            }
            if "amount" in request.data.keys():
                data.update(
                    {
                        "amount": request.data["amount"],
                        "overide_amount": True,
                    }
                )
            dbcart.add(**data, user=request.user.id)
            return Response(
                {"message": "dbcart is updated"},
                status=status.HTTP_202_ACCEPTED,
            )

        cart = Cart(request)
        if "amount" not in request.data.keys():
            cart.add(product_id=request.data["product"])
        else:
            cart.add(
                product_id=request.data["product"],
                amount=request.data["amount"],
                overide_amount=True,
            )

        return Response(
            {"message": "cart is updated"},
            status=status.HTTP_202_ACCEPTED,
        )

    def delete(self, request):
        if not request.user.is_anonymous:
            dbcart = DBCart(request)
            dbcart.clear()
            return Response(
                {"message": "dbcart is cleared"},
                status=status.HTTP_204_NO_CONTENT,
            )

        cart = Cart(request)
        cart.clear()
        return Response(
            {"message": "cart is cleared"},
            status=status.HTTP_204_NO_CONTENT,
        )

    def put(self, request):
        """
        Not documented method for manual transfering of session cart to DB.
        """
        cart = Cart(request)
        if not cart:
            return Response(
                {"message": "no cart in session"},
                status=status.HTTP_204_NO_CONTENT,
            )
        cart.build_cart(request.user)
        return Response(
            {"message": "cart uploaded to DB"},
            status=status.HTTP_201_CREATED,
        )


class CartDetailAPI(APIView):
    """
    Single API to handle cart operations
    """

    permission_classes = [permissions.AllowAny]
    message = "cart details updated"

    def patch(self, request, **kwargs):
        if not request.user.is_anonymous:
            DBCart(request)

            return Response(
                {"message": self.message},
                status=status.HTTP_205_RESET_CONTENT,
            )
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
