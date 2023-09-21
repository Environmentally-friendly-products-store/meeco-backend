from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.filters import ProductFilter
from api.pagination import Pagination
from api.permissions import IsAdminOrReadOnly

from .models import Event

from .serializers import FullEventSerializer, ShortEventSerializer


class EventViewSet(ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = ShortEventSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FullEventSerializer
        return self.serializer_class