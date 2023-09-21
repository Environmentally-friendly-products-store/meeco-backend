from django.db.models import Sum
from rest_framework import serializers

from users.models import ShoppingCart

from .models import Category, ImageSet, Product


class ShortProductSerializer(serializers.ModelSerializer):
    preview_image = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    category = serializers.StringRelatedField(read_only=True)
    # is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "price_per_unit",
            "preview_image",
            "category",
            "brand",
            "event",
            "is_in_shopping_cart",
            # 'is_favorited',
            "amount",
        )

    def get_preview_image(self, obj):
        if obj.images.exists():
            return obj.images.first().preview_image.url
        return None

    def get_amount(self, obj):
        user = self.context["request"].user

        if not user.is_anonymous:
            if ShoppingCart.objects.filter(user=user).exists():
                cart_items = ShoppingCart.objects.filter(user=user, product=obj)
                amount = cart_items.aggregate(Sum("amount"))["amount__sum"]
                return amount
        return 0

    def get_is_in_shopping_cart(self, obj):
        user = self.context["request"].user

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
    big_image = serializers.ImageField(source="big_image.url")
    preview_image = serializers.ImageField(source="preview_image.url")
    image_thumbnail = serializers.ImageField(source="image_thumbnail.url")

    class Meta:
        model = ImageSet
        fields = ("big_image", "preview_image", "image_thumbnail")

    def get_image_url(self, obj, image_type):
        return (
            f"/media/CACHE/product_images/{getattr(obj, image_type).name}"
            if getattr(obj, image_type)
            else None
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["big_image"] = self.get_image_url(instance, "big_image")
        data["preview_image"] = self.get_image_url(instance, "preview_image")
        data["image_thumbnail"] = self.get_image_url(instance, "image_thumbnail")
        return data


class FullProductSerializer(serializers.ModelSerializer):
    images = ImageSetSerializer(many=True, read_only=True)
    amount = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "price_per_unit",
            "name",
            "description",
            "images",
            # 'is_favorited',
            "is_in_shopping_cart",
            "category",
            "brand",
            "event",
            "amount",
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.context["request"].user

        return (
            user.is_authenticated
            and ShoppingCart.objects.filter(user=user, product=obj).exists()
        )

    def get_amount(self, obj):
        user = self.context["request"].user

        if not user.is_anonymous:
            if ShoppingCart.objects.filter(user=user).exists():
                cart_items = ShoppingCart.objects.filter(user=user, product=obj)
                amount = cart_items.aggregate(Sum("amount"))["amount__sum"]
                return amount
        return 0


class FullCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "description", "slug")


class ShortCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "description")
