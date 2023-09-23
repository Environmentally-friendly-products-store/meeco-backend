from rest_framework import viewsets

from api.pagination import Pagination
from orders.models import Order
from orders.serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = Pagination

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def perform_update(self, serializer):
        serializer.save(customer=self.request.user)
