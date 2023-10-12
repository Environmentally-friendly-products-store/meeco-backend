from rest_framework import serializers

from orders.models import Order, OrderProduct
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
        )


class OrderProductSerializer(serializers.ModelSerializer):
    product_id = ProductSerializer()
    # product_name = serializers.StringRelatedField(source="product.name")

    class Meta:
        model = OrderProduct
        fields = (
            "product_id",
            # "product_name",
            "amount",
            "purchase_price",
            "item_total",
        )
        read_only_fields = ("item_total",)


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    products = OrderProductSerializer(
        source="order_products", many=True, required=False
    )

    class Meta:
        model = Order
        fields = (
            "id",
            "customer",
            "contact_phone_number",
            "address",
            "price_total",
            "status",
            "comment",
            "products_count",
            "products",
        )
        read_only_fields = (
            "price_total",
            "products_count",
            "products",
        )

    def create(self, validated_data):
        return super().create(validated_data)


class CartProductSerializer(serializers.ModelSerializer):
    preview_image = serializers.SerializerMethodField()
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "preview_image",
            "category",
            "brand",
            "event",
        )

    def get_preview_image(self, obj):
        if obj.images.exists():
            return obj.images.first().preview_image.url
        return None
