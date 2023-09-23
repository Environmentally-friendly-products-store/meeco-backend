from collections import OrderedDict

from django.db.models import Sum
from djoser.serializers import UserSerializer
from rest_framework import serializers

from orders.models import Order, OrderProduct

# from products.serializers import ShortProductSerializer


class ItemTotalCalc(serializers.Field):
    """Поле для вычисления стоимости позиции в заказе."""

    def to_representation(self, value):
        return value

    def to_internal_value(self, obj):
        return round(obj.amount * obj.purchase_price, 2)


class OrderProductSerializer(serializers.ModelSerializer):
    # product_name = ShortProductSerializer(source="product_id")
    purchase_price = serializers.FloatField()
    item_total = ItemTotalCalc()

    class Meta:
        model = OrderProduct
        fields = (
            "id",
            "product_id",
            "amount",
            "purchase_price",
            "item_total",
        )
        read_only_fields = ("item_total",)


class OrderSerializer(serializers.ModelSerializer):
    article_number = serializers.CharField(
        required=False,
        default="",
    )
    customer = UserSerializer(
        default=serializers.CurrentUserDefault(),
        read_only=True,
    )
    delivery_address = serializers.CharField(source="address")
    products = OrderProductSerializer(
        required=False,
        many=True,
    )
    price_total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "id",
            "article_number",
            "customer",
            "contact_phone_number",
            "created_at",
            "delivery_address",
            "comment",
            "status",
            "price_total",
            "products",
        )
        read_only_fields = (
            "customer",
            "created_at",
            "price_total",
        )

    def to_representation(self, instance):
        result = super().to_representation(instance)
        return OrderedDict(
            [(key, result[key]) for key in result if result[key] not in [None, ""]]
        )

    def get_price_total(self, obj):
        return obj.products.aggregate(Sum("item_total"))["item_total__sum"]

    # def create(self, validated_data):
    #     if "products" not in self.initial_data:
    #         order = Order.objects.create(**validated_data)
    #         return order
    #     products = validated_data.pop("products")
    #     order = Order.objects.create(**validated_data)
    #     for product in products:
    #         current_product, status = OrderProduct.objects.get_or_create(
    #             **product,
    #         )
    #         OrderProduct.objects.create(
    #             order_id=order,
    #             product_id=current_product.id,
    #             amount=current_product.amount,
    #             purchase_price=current_product.purchase_price,
    #         )
    #     return order
