from django.contrib import admin
from orders.models import DeliveryAddress, OrderProduct, Order

admin.site.register(DeliveryAddress)


@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "country",
        "city",
        "street",
        "house",
        "apartment",
    )


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order_id",
        "product_id",
        "amount",
        "street",
        "purchase_price",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "article_number",
        "customer",
        "address",
        "created_at",
        "price_total",
        "status",
        "comment",
    )
