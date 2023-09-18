from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from rest_framework import mixins, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import CustomCreateSerializer

User = get_user_model()


class UserRegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CustomCreateSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer) -> None:
        if "username" in self.request.data:
            username = self.request.data["username"]
        else:
            username = "NoUserName"
        serializer.save(username=username)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request, *args, **kwargs):
    user = get_object_or_404(User, pk=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data)
