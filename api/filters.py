from django_filters.rest_framework import FilterSet, filters

from events.models import Event
from products.models import Brand, Category, Product
from users.models import Favorite, ShoppingCart


class ProductFilter(FilterSet):
    name = filters.CharFilter(field_name="name")
    category = filters.ModelMultipleChoiceFilter(
        field_name="category__slug",
        to_field_name="slug",
        queryset=Category.objects.all(),
    )
    brand = filters.ModelMultipleChoiceFilter(
        field_name="brand__slug",
        to_field_name="slug",
        queryset=Brand.objects.all(),
    )
    event = filters.ModelMultipleChoiceFilter(
        field_name="event__slug",
        to_field_name="slug",
        queryset=Event.objects.all(),
    )
    price_per_unit = filters.NumberFilter()
    min_price = filters.NumberFilter(field_name="price_per_unit", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price_per_unit", lookup_expr="lte")
    is_in_shopping_cart = filters.BooleanFilter(method="get_is_in_shopping_cart")
    is_favorite = filters.BooleanFilter(method="get_is_favorite")

    class Meta:
        model = Product
        fields = (
            "name",
            "category",
            "brand",
            "min_price",
            "max_price",
            "is_in_shopping_cart",
            "event",
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.request.user

        if not user.is_anonymous:
            return ShoppingCart.objects.filter(user=user, product=obj).exists()
        return False

    def get_is_favorite(self, obj):
        user = self.request.user

        if not user.is_anonymous:
            return Favorite.objects.filter(user=user, product=obj).exists()
        return False
