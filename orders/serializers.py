from django.db.models import Sum
from djoser.serializers import UserSerializer
from rest_framework import serializers

from orders.models import Order, OrderProduct
from products.models import Product


class ItemTotalCalc(serializers.Field):
    """Поле для вычисления стоимости позиции в заказе."""

    def to_representation(self, value):
        return value

    def to_internal_value(self, obj):
        return round(obj.amount * obj.purchase_price, 2)


class OrderProductSerializer(serializers.ModelSerializer):
    product_name = serializers.StringRelatedField(source="product_id")
    purchase_price = serializers.FloatField()
    item_total = ItemTotalCalc()

    class Meta:
        model = OrderProduct
        fields = (
            "id",
            "product_name",
            "amount",
            "purchase_price",
            "item_total",
        )
        read_only_fields = (
            "product_name",
            "item_total",
        )


class OrderSerializer(serializers.ModelSerializer):
    article_number = serializers.CharField(required=False)
    customer = UserSerializer(default=serializers.CurrentUserDefault())
    delivery_address = serializers.CharField(source="address")
    products = OrderProductSerializer(
        many=True,
        required=False,
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
            "price_total",
        )

    def get_price_total(self, obj):
        return obj.products.aggregate(Sum("item_total"))["item_total__sum"]

    def create(self, validated_data):
        if "products" not in self.initial_data:
            order = Order.objects.create(**validated_data)
            return order
        products = validated_data.pop("products")
        order = Order.objects.create(**validated_data)
        for product in products:
            current_product, status = Product.objects.get_or_create(
                **product,
            )
            OrderProduct.objects.create(
                order_id=order,
                customer=self.user,
                product_id=current_product,
                amount=current_product["amount"],
                purchase_price=current_product["purchase_price"],
            )
        return order
