from rest_framework import serializers

from orders import appvars as VARS
from orders.models import Order, OrderProduct
from products.models import Product
from users.models import ShoppingCart


class CartProductSerializer(serializers.ModelSerializer):
    preview_image = serializers.SerializerMethodField()
    category = serializers.StringRelatedField(read_only=True)
    brand = serializers.StringRelatedField(read_only=True)

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
        )

    def get_preview_image(self, obj):
        if obj.images.exists():
            return obj.images.first().preview_image.url
        return None


class DBCartSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = (
            "user",
            "amount",
            "total_price",
            "product",
        )

    def get_total_price(self, obj):
        return obj.product.price_per_unit * obj.amount


class OrderProductSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(source="product_id")
    # product_name = serializers.StringRelatedField(source="product.name")

    class Meta:
        model = OrderProduct
        fields = (
            "amount",
            "purchase_price",
            "item_total",
            "product",
            # "product_name",
        )
        read_only_fields = ("item_total",)


class OrderStatusField(serializers.ChoiceField):
    def to_internal_value(self, data):
        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail("invalid_choice", input=data)


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    status = OrderStatusField(choices=VARS.ORDER_STATUSES)
    products = OrderProductSerializer(
        source="order_products", many=True, required=False
    )

    class Meta:
        model = Order
        fields = (
            "id",
            "created_at",
            "customer",
            "contact_phone_number",
            "address",
            "status",
            "comment",
            "price_total",
            "products_count",
            "products",
        )
        read_only_fields = (
            "price_total",
            "products_count",
            "products",
        )
