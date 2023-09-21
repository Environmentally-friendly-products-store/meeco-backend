from django.contrib.auth import get_user_model
from rest_framework import serializers

from products.models import Product

User = get_user_model()


class UserProductSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        fields = ["user", "product"]
