from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend


from api.filters import ProductFilter
from api.pagination import Pagination
from api.permissions import IsAdminOrReadOnly
from .models import Product
from .serializers import ShortProductSerializer, FullProductSerializer


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ShortProductSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FullProductSerializer
        return self.serializer_class