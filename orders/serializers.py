from rest_framework import serializers

from orders.appvars import DEL_ADDR_COUNTRIES
from orders.models import DeliveryAddress, Order, OrderProduct
from products.models import Product
from products.serializers import ShortProductSerializer


class DeliveryAddressSerializer(serializers.ModelSerializer):
    country = serializers.ChoiceField(choices=DEL_ADDR_COUNTRIES)

    class Meta:
        model = DeliveryAddress
        fields = (
            "id",
            "owner",
            "country",
            "city",
            "street",
            "house",
            "apartment",
        )


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField()
    address = serializers.StringRelatedField()
    products = ShortProductSerializer(
        many=True,
        required=False,
    )

    class Meta:
        model = Order
        fields = (
            "id",
            "customer",
            "address",
            "created_at",
            "price_result",
            "status",
            "comment",
            "products",
        )

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
                product_id=current_product,
                amount=current_product["amount"],
                purchase_price=current_product["purchase_price"],
            )
        return order


class OrderProductSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()

    class Meta:
        model = OrderProduct
        fields = (
            "id",
            "order_id",
            "product_id",
            "amount",
            "purchase_price",
            "result",
        )

    def get_result(self, obj):
        return obj.amount * obj.purchase_price
