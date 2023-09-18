from rest_framework import serializers
from django.db.models import Sum

from .models import Product, ImageSet
from users.models import ShoppingCart


class ShortProductSerializer(serializers.ModelSerializer):
    preview_image = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    category = serializers.StringRelatedField(read_only=True)
    # is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price_per_unit',
            'preview_image',
            'category',
            'brand',
            'event',
            'is_in_shopping_cart',
            # 'is_favorited',
            'amount'
        )

    def get_preview_image(self, obj):
        if obj.images.exists():
            return obj.images.first().preview_image.url
        return None

    def get_amount(self, obj):
        user = self.context['request'].user

        if ShoppingCart.objects.filter(user=user).exists():
            cart_items = ShoppingCart.objects.filter(user=user, product=obj)
            amount = cart_items.aggregate(Sum('amount'))['amount__sum']
            return amount
        return 0

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user

        return (
            user.is_authenticated
            and ShoppingCart.objects.filter(user=user, product=obj).exists()
        )
#     def get_is_favorited(self, obj):
#     user = self.context['request'].user

#     return (
#         user.is_authenticated
#         and Favorite.objects.filter(user=user, product=obj).exists()
#     )


class ImageSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageSet
        fields = ('big_image', 'preview_image', 'image_thumbnail')


class FullProductSerializer(serializers.ModelSerializer):
    images = ImageSetSerializer(many=True, read_only=True, source='CACHE/images/product_images')
    amount = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'price_per_unit',
            'name',
            'description',
            'images',
            # 'is_favorited',
            'is_in_shopping_list',
            'category',
            'brand',
            'event',
            'amount'
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user

        return (
            user.is_authenticated
            and ShoppingCart.objects.filter(user=user, product=obj).exists()
        )

    def get_amount(self, obj):
        user = self.context['request'].user

        if ShoppingCart.objects.filter(user=user).exists():
            cart_items = ShoppingCart.objects.filter(user=user, product=obj)
            amount = cart_items.aggregate(Sum('amount'))['amount__sum']
            return amount
        return 0
