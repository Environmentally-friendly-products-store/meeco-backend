from django.contrib import admin

from orders.models import Order, OrderProduct


class OrderProductLine(admin.TabularInline):
    model = OrderProduct
    min_num = 1
    max_num = 200
    extra = 1
    raw_id_fields = ["product"]


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderProductLine,)
    list_display = (
        "id",
        "article_number",
        "customer",
        "address",
        "price_total",
        "status",
        "comment",
        "created_at",
    )
    list_filter = ("customer", "status", "created_at")
    list_editable = ("status",)
    search_fields = ("price_total",)
    empty_value_display = "-пусто-"


admin.site.register(Order, OrderAdmin)


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "order",
        "amount",
        "purchase_price",
        "item_total",
    )
    list_editable = (
        "product",
        "order",
        "amount",
    )
    search_fields = ("order",)
    empty_value_display = "-пусто-"
