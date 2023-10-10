from django.contrib import admin

from products.models import Brand, Category, ImageSet, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "category",
        "brand",
        "event",
        "price_per_unit",
        "view_amount",
        "buy_amount",
    )
    list_editable = (
        "name",
        "description",
        "category",
        "brand",
        "event",
        "price_per_unit",
    )
    list_filter = (
        "name",
        "category",
        "brand",
        "event",
        "view_amount",
        "buy_amount",
    )
    search_fields = ("name",)
    empty_value_display = "-пусто-"


@admin.register(ImageSet)
class ImageSetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "image",
    )
    list_editable = ("image",)
    search_fields = ("product",)
    empty_value_display = "-пусто-"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("id", "name", "description", "slug")
    list_editable = (
        "name",
        "description",
    )
    list_filter = ("name",)
    search_fields = ("name",)
    empty_value_display = "-пусто-"


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("id", "name", "description", "country", "slug")
    list_editable = (
        "name",
        "description",
        "country",
    )
    list_filter = ("name",)
    search_fields = ("name",)
    empty_value_display = "-пусто-"
