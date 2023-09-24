from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.pagination import Pagination
from orders.models import Order
from orders.serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("customer").all()
    serializer_class = OrderSerializer
    pagination_class = Pagination
    permission_classes = [permissions.IsAuthenticated]

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
