from rest_framework import viewsets

from orders.models import DeliveryAddress, Order
from orders.serializers import DeliveryAddressSerializer, OrderSerializer


class DeliveryAddressViewSet(viewsets.ModelViewSet):
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryAddressSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
