from decimal import Decimal

from django.db.models import Count, Sum
from rest_framework import serializers

from orders.models import Order, OrderProduct


class OrderProductSerializer(serializers.ModelSerializer):
    product_name = serializers.StringRelatedField(source="product_id")
    purchase_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    item_total = serializers.SerializerMethodField()

    class Meta:
        model = OrderProduct
        fields = (
            "id",
            "product_name",
            "amount",
            "purchase_price",
            "item_total",
        )
        read_only_fields = ("item_total",)

    def get_item_total(self, obj):
        return Decimal(obj.amount * obj.purchase_price)


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    delivery_address = serializers.CharField(source="address")
    price_total = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "id",
            "customer",
            "contact_phone_number",
            "delivery_address",
            "comment",
            "status",
            "price_total",
            "products_count",
        )
        read_only_fields = (
            "price_total",
            "products_count",
        )

    def get_price_total(self, obj):
        return obj.products.aggregate(Sum("item_total"))["item_total__sum"]

    def get_products_count(self, obj):
        return obj.products.aggregate(Count("id"))["id__count"]
