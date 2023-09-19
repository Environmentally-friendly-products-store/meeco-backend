from rest_framework import serializers

# from orders.appvars import DEL_ADDR_COUNTRIES
# from orders.models import DeliveryAddress
from orders.models import Order, OrderProduct
from products.models import Product


class OrderProductSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    product_name = serializers.StringRelatedField(
        source="product_id",
        read_only=True,
    )

    class Meta:
        model = OrderProduct
        fields = (
            "id",
            "product_name",
            "amount",
            "purchase_price",
            "total",
        )

    def get_total(self, obj):
        return obj.amount * obj.purchase_price


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField()
    products = OrderProductSerializer(
        many=True,
        required=False,
    )

    class Meta:
        model = Order
        fields = (
            "id",
            "article_number",
            "customer",
            "address",
            "created_at",
            "price_total",
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
