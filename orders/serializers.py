from django.db.models import Sum
from rest_framework import serializers

from orders.models import Order, OrderProduct
from products.models import Product


class OrderProductSerializer(serializers.ModelSerializer):
    item_total = serializers.SerializerMethodField()
    product_name = serializers.StringRelatedField(
        source="product_id",
        read_only=True,
    )
    purchase_price = serializers.FloatField()

    class Meta:
        model = OrderProduct
        fields = (
            "id",
            "product_name",
            "amount",
            "purchase_price",
            "item_total",
        )

    def get_item_total(self, obj):
        return round(obj.amount * obj.purchase_price, 2)


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField()
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
            "created_at",
            "address",
            "comment",
            "status",
            "price_total",
            "products",
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
                product_id=current_product,
                amount=current_product["amount"],
                purchase_price=current_product["purchase_price"],
            )
        return order


# class DeliveryAddressSerializer(serializers.ModelSerializer):
#     country = serializers.ChoiceField(choices=DEL_ADDR_COUNTRIES)

#     class Meta:
#         model = DeliveryAddress
#         fields = (
#             "id",
#             "owner",
#             "country",
#             "city",
#             "street",
#             "house",
#             "apartment",
#         )
