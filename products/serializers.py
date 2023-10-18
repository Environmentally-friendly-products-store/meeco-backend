from django.db.models import Sum
from rest_framework import serializers

from core.serializers import SLUG_MODEL_FIELDS, SlugModelSerializer
from events.serializers import FullEventSerializer, ShortEventSerializer
from users.models import Favorite, ShoppingCart

from .models import Brand, Category, ImageSet, Product


class ShortCategorySerializer(SlugModelSerializer):
    class Meta(SlugModelSerializer.Meta):
        model = Category


class ShortBrandSerializer(SlugModelSerializer):
    class Meta(SlugModelSerializer.Meta):
        model = Brand


class FullCategorySerializer(ShortCategorySerializer):
    class Meta(ShortCategorySerializer.Meta):
        fields = SLUG_MODEL_FIELDS + ("id", "description")


class FullBrandSerializer(ShortBrandSerializer):
    class Meta(ShortBrandSerializer.Meta):
        fields = SLUG_MODEL_FIELDS + ("id", "description", "country")


class ImageSetSerializer(serializers.ModelSerializer):
    big_image = serializers.ImageField(source="big_image.url")
    preview_image = serializers.ImageField(source="preview_image.url")
    image_thumbnail = serializers.ImageField(source="image_thumbnail.url")

    class Meta:
        model = ImageSet
        fields = ("big_image", "preview_image", "image_thumbnail")

    @staticmethod
    def _get_image_url(obj, image_type):
        return getattr(obj, image_type).url if getattr(obj, image_type) else None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["big_image"] = self._get_image_url(instance, "big_image")
        data["preview_image"] = self._get_image_url(instance, "preview_image")
        data["image_thumbnail"] = self._get_image_url(instance, "image_thumbnail")
        return data


PRODUCT_FIELDS = (
    "id",
    "name",
    "price_per_unit",
    "category",
    "brand",
    "event",
)

PRODUCT_MIXIN_FIELDS = (
    "is_in_shopping_cart",
    "is_favorite",
    "amount",
)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = PRODUCT_FIELDS + PRODUCT_MIXIN_FIELDS


class ProductMixinSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    def _get_user(self):
        return self.context["request"].user

    def get_amount(self, obj):
        user = self._get_user()
        if not user.is_anonymous:
            if ShoppingCart.objects.filter(user=user).exists():
                cart_items = ShoppingCart.objects.filter(user=user, product=obj)
                amount = cart_items.aggregate(Sum("amount"))["amount__sum"]
                return amount
        return 0

    def get_is_in_shopping_cart(self, obj):
        user = self._get_user()
        if not user.is_anonymous:
            return ShoppingCart.objects.filter(user=user, product=obj).exists()
        return False

    def get_is_favorite(self, obj):
        user = self._get_user()
        if not user.is_anonymous:
            return Favorite.objects.filter(user=user, product=obj).exists()
        return False


class ShortProductSerializer(ProductSerializer, ProductMixinSerializer):
    preview_image = serializers.SerializerMethodField()
    category = ShortCategorySerializer()
    brand = ShortBrandSerializer()
    event = ShortEventSerializer()

    class Meta(ProductSerializer.Meta):
        fields = PRODUCT_FIELDS + PRODUCT_MIXIN_FIELDS + ("preview_image",)

    @staticmethod
    def get_preview_image(obj):
        if obj.images.exists():
            return obj.images.first().preview_image.url
        return None


class FullProductSerializer(ProductSerializer, ProductMixinSerializer):
    images = ImageSetSerializer(many=True, read_only=True)
    category = FullCategorySerializer()
    brand = FullBrandSerializer()
    event = FullEventSerializer()

    class Meta(ProductSerializer.Meta):
        fields = PRODUCT_FIELDS + PRODUCT_MIXIN_FIELDS + ("images",)
