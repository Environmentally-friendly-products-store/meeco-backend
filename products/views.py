from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Product
from .serializers import ShortProductSerializer, FullProductSerializer


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ShortProductSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FullProductSerializer
        return self.serializer_class
