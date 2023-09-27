from collections import OrderedDict

from django.db.models import Count, Sum
from djoser.serializers import UserSerializer
from rest_framework import serializers

from orders.models import Order, OrderProduct


class OrderProductSerializer(serializers.ModelSerializer):
    product_name = serializers.StringRelatedField(source="product_id")
    purchase_price = serializers.FloatField()
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
        return round(obj.amount * obj.purchase_price, 2)

    def create(self, validated_data):
        item_total = validated_data.get("amount") * validated_data.get("purchase_price")
        validated_data.update(
            {
                "item_total": item_total,
            }
        )
        return super().create(validated_data)


class OrderListSerializer(serializers.ModelSerializer):
    """
    Для отображения списка заказов как текущего пользователя, так и всех заказов в системе.
    Используется сокращенный набор полей.

    """

    article_number = serializers.CharField(
        allow_null=True,
        required=False,
    )
    customer = UserSerializer(
        default=serializers.CurrentUserDefault(),
        read_only=True,
    )
    delivery_address = serializers.CharField(source="address")
    price_total = serializers.SerializerMethodField()
    products = OrderProductSerializer(
        required=False,
        many=True,
    )

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

    def get_price_total(self, obj):
        return obj.products.aggregate(Sum("item_total"))["item_total__sum"]

    # def get_customer(self, obj):
    #     return self.context["request"].user in obj.customer_id.all()

    def to_representation(self, instance):
        result = super().to_representation(instance)
        return OrderedDict(
            [
                (key, result[key])
                for key in result
                if result[key]
                not in [
                    None,
                    "",
                ]
            ]
        )

    def create(self, validated_data):
        if "products" not in self.initial_data:
            order = Order.objects.create(**validated_data)
            return order
        products = validated_data.pop("products")
        order = Order.objects.create(**validated_data)
        for product in products:
            OrderProduct.objects.create(order_id=order, **product)
        return order

    def update(self, instance, validated_data):
        instance.article_number = validated_data.get(
            "article_number", instance.article_number
        )
        instance.contact_phone_number = validated_data.get(
            "contact_phone_number", instance.contact_phone_number
        )
        instance.address = validated_data.get("address", instance.address)
        instance.status = validated_data.get("status", instance.status)
        instance.comment = validated_data.get("comment", instance.comment)
        if "products" in validated_data:
            products = validated_data.pop("products")
            lst = []
            for product in products:
                current_product, status = OrderProduct.objects.get_or_create(**product)
                lst.append(current_product)
            instance.products.set(lst)

        instance.save()
        return instance


class OrderSerializer(OrderListSerializer):
    """
    Используется для создания нового заказа, просмотра, обновления информации
    по конкретному заказу и его удаления.

    """

    customer = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "id",
            "contact_phone_number",
            "delivery_address",
            "comment",
            "status",
            "price_total",
            "products",
        )
        read_only_fields = (
            "price_total",
            "products",
        )

    def get_products(self, obj):
        return obj.products.aggregate(Count("id"))["id__count"]
