from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from .models import Ingredient, Recipe

User = get_user_model()


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )
    is_favorited = filters.BooleanFilter(method='get_favorite')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'tags', 'author', 'is_in_shopping_cart',)

    def get_favorite(self, value):
        user = self.request.user
        if value:
            return Recipe.objects.filter(favorites__user=user).distinct()
        return Recipe.objects.all()

    def get_is_in_shopping_cart(self, value):
        user = self.request.user
        if value:
            return Recipe.objects.filter(shopping_cart__user=user)
        return Recipe.objects.all()


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name',)
