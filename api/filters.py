from django_filters.rest_framework import FilterSet, filters

from events.models import Event
from products.models import Category, Product


class ProductFilter(FilterSet):
    category = filters.ModelMultipleChoiceFilter(
        field_name="category__slug",
        to_field_name="slug",
        queryset=Category.objects.all(),
    )
    event = filters.ModelMultipleChoiceFilter(
        field_name="event__slug",
        to_field_name="slug",
        queryset=Event.objects.all(),
    )
    is_in_shopping_cart = filters.BooleanFilter(method="get_is_in_shopping_cart")

    class Meta:
        model = Product
        fields = ("category", "is_in_shopping_cart", "event")

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user

        if value and not user.is_anonymous:
            return queryset.filter(user_product__user=user)

        return queryset
