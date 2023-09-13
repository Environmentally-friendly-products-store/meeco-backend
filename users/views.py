from django.contrib.auth import get_user_model

from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from djoser.serializers import UserCreateSerializer


User = get_user_model()


class UserRegisterViewSet(mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer) -> None:
        if 'username' in self.request.data:
            username = self.request.data['username']
        else:
            username = 'NoUserName'
        serializer.save(username=username)
