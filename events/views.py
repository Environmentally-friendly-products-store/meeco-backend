from rest_framework.viewsets import ReadOnlyModelViewSet

from api.permissions import IsAdminOrReadOnly

from .models import Event
from .serializers import EventSerializer


class EventViewSet(ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
