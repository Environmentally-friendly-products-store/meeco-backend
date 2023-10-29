from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.filters import ProductFilter
from api.pagination import Pagination
from api.permissions import IsAdminOrReadOnly

from .models import Brand, Category, Product
from .serializers import (
    FullBrandSerializer,
    FullCategorySerializer,
    FullProductSerializer,
    ShortProductSerializer,
)


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ShortProductSerializer
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    filterset_class = ProductFilter
    # ordering_fields = ("price_per_unit",)
    search_fields = ("$name",)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FullProductSerializer
        return self.serializer_class


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = FullCategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class BrandViewSet(ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = FullBrandSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
