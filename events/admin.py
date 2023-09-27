from django.contrib import admin

from .models import Event

# from products.models import ProductEvent



# class ProductEventInline(admin.TabularInline):
#     model = ProductEvent
#     min_num = 1
#     max_num = 200
#     extra = 1


class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    # inlines = (ProductEventInline,)
    list_display = (
        "id",
        "name",
        "description",
        "image",
        "discount",
        "date_start",
        "date_end",
    )
    list_filter = ("name", "discount", "date_start", "date_end")
    list_editable = ("name", "description", "discount",
                     "date_start", "date_end")
    search_fields = ("name",)
    empty_value_display = "-пусто-"


admin.site.register(Event, EventAdmin)


# @admin.register(ProductEvent)
# class ProductEventAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "product_id",
#         "event_id",
#     )
#     list_editable = (
#         "product_id",
#         "event_id",
#     )
#     search_fields = ("event_id",)
#     empty_value_display = "-пусто-"
