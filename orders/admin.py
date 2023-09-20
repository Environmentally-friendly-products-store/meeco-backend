from django.contrib import admin

from orders.models import Order, OrderProduct


class OrderProductLine(admin.TabularInline):
    model = OrderProduct
    min_num = 1
    max_num = 200
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderProductLine,)
    list_display = (
        "id",
        "article_number",
        "customer",
        "address",
        "grand_total",
        "status",
        "comment",
        "created_at",
    )
    list_filter = ("article_number", "customer", "status", "created_at")
    list_editable = ("status",)
    search_fields = ("article_number",)
    empty_value_display = "-пусто-"


admin.site.register(Order, OrderAdmin)


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product_id",
        "order_id",
        "amount",
        "purchase_price",
    )
    list_editable = (
        "product_id",
        "order_id",
        "amount",
    )
    search_fields = ("order_id",)
    empty_value_display = "-пусто-"
