from rest_framework import viewsets

# from orders.models import DeliveryAddress
# from orders.serializers import DeliveryAddressSerializer
from api.pagination import Pagination
from orders.models import Order
from orders.serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = Pagination


# class DeliveryAddressViewSet(viewsets.ModelViewSet):
#     queryset = DeliveryAddress.objects.all()
#     serializer_class = DeliveryAddressSerializer
