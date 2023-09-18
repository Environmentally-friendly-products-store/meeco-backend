from django.contrib import admin

from orders.models import DeliveryAddress, Order, OrderProduct


@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "owner",
        "country",
        "city",
        "street",
        "house",
        "apartment",
    )
    list_editable = ("owner",)


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "order_id",
        "product_id",
        "amount",
        "purchase_price",
    )
    list_editable = (
        "order_id",
        "product_id",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "customer",
        "address",
        "created_at",
        "price_total",
        "status",
        "comment",
    )
    list_editable = (
        "customer",
        "address",
    )
