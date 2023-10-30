from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportMixin

from products.models import Brand, Category, ImageSet, Product


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        exclude = ("created_at", "view_amount", "buy_amount")
        export_order = (
            "id",
            "name",
            "description",
            "price_per_unit",
            "discount",
            "long_name",
            "structure",
            "category",
            "brand",
            "event",
        )


@admin.register(Product)
class ProductAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "long_name",
        "structure",
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
        "long_name",
        "structure",
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
    resource_classes = [ProductResource]


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
