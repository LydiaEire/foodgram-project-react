from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register(
    r'recipes/(?P<id>\d+)/favorite',
    FavoriteViewSet, basename='recipe_favorite'
)
router.register(
    'recipes/download_shopping_cart',
    ShoppingCartViewSet, basename='recipes_download_shopping_cart'
)
router.register(
    r'recipes/(?P<id>\d+)/shopping_cart',
    ShoppingCartViewSet, basename='recipe_shopping_cart'
)


urlpatterns = [
    path('', include(router.urls))
]