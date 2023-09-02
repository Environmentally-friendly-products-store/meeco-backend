import django_filters as filters

from recipes.models import (
    Ingredients,
    Recipes,
    Tags,
)


class RecipesFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tags.objects.all(),
    )
    is_favorited = filters.CharFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = filters.CharFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipes
        fields = [
            'author',
            'tags',
            'is_favorited',
            'is_in_shopping_cart'
        ]

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            return Recipes.objects.filter(favorite__user=user)
        return Recipes.objects.all()

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return Recipes.objects.filter(shoppingcart__user=user)
        return Recipes.objects.all()


class IngredientsFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='startswith'
    )

    class Meta:
        model = Ingredients
        fields = ['name']
