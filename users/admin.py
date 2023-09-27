from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import ShoppingCart

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "date_joined",
        "last_login",
    )
    list_editable = ("first_name", "last_name", "is_staff")
    list_filter = ("email", "is_staff", "date_joined", "last_login")
    search_fields = ("email",)
    empty_value_display = "-пусто-"


# @admin.register(Favorite)
# class FavoriteAdmin(admin.ModelAdmin):
#     list_display = ("id", "user", "product")
#     list_filter = ("user", "product",)
#     search_fields = ("user",)
#     empty_value_display = "-пусто-"


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "amount")
    list_editable = ("amount",)
    list_filter = (
        "user",
        "product",
    )
    search_fields = ("user",)
    empty_value_display = "-пусто-"
