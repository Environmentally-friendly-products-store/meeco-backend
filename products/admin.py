from django.contrib import admin

from products.models import Brand, Category, Favorite, Product, ShoppingCart


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "brand")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product")


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "amount")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "country", "slug")
