from django.contrib.auth import get_user_model
from django_filters import CharFilter
from django_filters import rest_framework as filters

from .models import Ingredient, Recipe

User = get_user_model()


class RecipeFilter(filters.FilterSet):
    tags = CharFilter(field_name='tags__slug', method='filter_tags')
    is_favorited = filters.BooleanFilter(method='get_favorite')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags')

    def filter_tags(self, queryset, slug, tags):
        tags = self.request.query_params.getlist('tags')
        return queryset.filter(
            tags__slug__in=tags
        ).distinct()

    def get_favorite(self, queryset, value, is_favorited, slug=None):
        user = self.request.user
        if not user.is_authenticated:
            return queryset
        if is_favorited:
            return queryset.filter(
                favorites__user=self.request.user
            ).distinct()
        return queryset

    def get_is_in_shopping_cart(
            self, queryset, value,
            is_in_shopping_cart):
        user = self.request.user
        if not user.is_authenticated:
            return queryset
        if is_in_shopping_cart:
            return queryset.filter(
                shopping_cart__user=self.request.user
            ).distinct()
        return queryset


class IngredientFilter(filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ('name',)
