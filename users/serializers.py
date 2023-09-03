from django.contrib.auth import get_user_model

from rest_framework import serializers


User = get_user_model()

USER_FIELDS = [
    'email',
    'id',
    'username',
    'first_name',
    'last_name',
]


class CoreUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class PostUserSerializer(CoreUserSerializer):
    class Meta(CoreUserSerializer.Meta):
        fields = USER_FIELDS


class GetUserSerializer(CoreUserSerializer):
    class Meta(CoreUserSerializer.Meta):
        fields = USER_FIELDS


class PasswordSerializer(CoreUserSerializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    class Meta(CoreUserSerializer.Meta):
        fields = ['new_password', 'current_password']