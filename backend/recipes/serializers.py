from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.serializers import UserSerializerModified
from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag, TagsInRecipe)

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    color = serializers.CharField(source='hexcolor')

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class ShowRecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializerModified()
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_ingredients(self, obj):
        qs = IngredientInRecipe.objects.filter(recipe=obj)
        return IngredientInRecipeSerializer(qs, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return Favorite.objects.filter(recipe=obj, user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return ShoppingCart.objects.filter(recipe=obj, user=user).exists()


class AddIngredientToRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class CreateRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(represent_in_base64=True)
    author = UserSerializerModified(read_only=True)
    ingredients = AddIngredientToRecipeSerializer(many=True)
    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='id'
    )
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time')

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        for item in ingredients:
            if int(item['amount']) < 0:
                raise serializers.ValidationError(
                    {
                        'ingredients': (
                            'Убедитесь, что количество больше 0')
                    }
                )
        return data

    def validate_cooking_time(self, data):
        if data <= 0:
            raise serializers.ValidationError(
                'Введите целое число больше 0'
            )
        return data

    def create(self, validated_data):

        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(author=author, **validated_data)
        for ingredient in ingredients_data:
            ingredient_model = ingredient['id']
            amount = ingredient['amount']
            IngredientInRecipe.objects.create(
                ingredient=ingredient_model,
                recipe=recipe,
                amount=amount
            )
        for tag in tags_data:
            TagsInRecipe.objects.create(recipe=recipe, tag=tag)
        return recipe

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags')
        ingredient_data = validated_data.pop('ingredients')
        IngredientInRecipe.objects.filter(recipe=instance).delete()
        instance.name = validated_data.pop('name')
        instance.text = validated_data.pop('text')
        if validated_data.get('image') is not None:
            instance.image = validated_data.get('image')
        instance.cooking_time = validated_data.pop('cooking_time')
        instance.save()
        instance.tags.set(tags_data)

        for new_ingredient in ingredient_data:
            IngredientInRecipe.objects.create(
                ingredient=new_ingredient['id'],
                recipe=instance,
                amount=new_ingredient['amount']
            )
        return instance

    def to_representation(self, instance):
        return ShowRecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }).data


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        method = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            method = request.method
        if method == 'DELETE':
            if not Favorite.objects.filter(user=data.get('user'),
                                           recipe=data.get('recipe')).exists():
                raise serializers.ValidationError("Не в избранном")
        else:
            if Favorite.objects.filter(user=data.get('user'),
                                       recipe=data.get('recipe')).exists():
                raise serializers.ValidationError("Уже в избранном")
        return data


class ShoppingCartSerializer(FavoriteSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate(self, data):
        method = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            method = request.method
        if method == 'DELETE':
            if not ShoppingCart.objects.filter(
                    user=data.get('user'),
                    recipe=data.get(
                        'recipe')).exists():
                raise serializers.ValidationError("Не в корзине")
        else:
            if ShoppingCart.objects.filter(user=data.get('user'),
                                           recipe=data.get('recipe')).exists():
                raise serializers.ValidationError("Уже в корзине")
        return data

    class Meta(FavoriteSerializer.Meta):
        model = ShoppingCart
