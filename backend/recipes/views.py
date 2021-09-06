from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)
from .permissions import AdminOrAuthorOrReadOnly
from .serializers import (CreateRecipeSerializer, FavoriteSerializer,
                          IngredientSerializer, ShoppingCartSerializer,
                          ShowRecipeSerializer, TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny, ]
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_class = IngredientFilter
    search_fields = ('name', )
    pagination_class = None

    def get_queryset(self):
        return Ingredient.objects.filter()


class RecipeResultsSetPagination(PageNumberPagination):
    page_size = 6

    def paginate_queryset(self, queryset, request, view=None):
        is_in_shopping_cart = request.query_params.get(
            'is_in_shopping_cart',
        )
        if is_in_shopping_cart:
            self.page_size = 999
        return super().paginate_queryset(queryset, request, view)


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminOrAuthorOrReadOnly, ]
    filter_class = RecipeFilter
    filter_backends = (SearchFilter, DjangoFilterBackend)
    pagination_class = RecipeResultsSetPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShowRecipeSerializer
        return CreateRecipeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_queryset(self):
        return Recipe.objects.filter()


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, ]

    def add(self, request, recipe_id):
        user = request.user
        data = {
            "user": user.id,
            "recipe": recipe_id,
        }

        serializer = FavoriteSerializer(
            data=data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def remove(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        data = {
            "user": user.id,
            "recipe": recipe_id,
        }
        serializer = FavoriteSerializer(
            data=data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        Favorite.objects.get(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = ShoppingCart.objects.all()
    serializer_class = ShowRecipeSerializer

    def add(self, request, recipe_id):
        user = request.user
        data = {
            "user": user.id,
            "recipe": recipe_id,
        }
        context = {'request': request}
        serializer = ShoppingCartSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def remove(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        data = {
            "user": user.id,
            "recipe": recipe_id,
        }
        context = {'request': request}
        serializer = ShoppingCartSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        ShoppingCart.objects.get(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def download_shopping_cart(request):
    user = request.user
    shopping_cart = user.shopping_cart.all()
    buying_list = {}
    for record in shopping_cart:
        recipe = record.recipe
        ingredients = IngredientInRecipe.objects.filter(recipe=recipe)
        for ingredient in ingredients:
            amount = ingredient.amount
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit
            if name not in buying_list:
                buying_list[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount
                }
            else:
                buying_list[name]['amount'] = (buying_list[name]['amount']
                                               + amount)
    wishlist = []
    for name, data in buying_list.items():
        wishlist.append(
            f"{name} - {data['amount']} ({data['measurement_unit']} \n")
    response = HttpResponse(wishlist, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="wishlist.txt"'
    return response
