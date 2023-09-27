from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.pagination import Pagination
from api.permissions import IsOwnerOrReadOnly
from orders.models import Order
from orders.serializers import OrderListSerializer, OrderSerializer


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
                for permission in self.permission_classes_by_action[
                    self.action]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]
