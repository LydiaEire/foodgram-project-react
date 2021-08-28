from django.contrib.auth import authenticate, get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from foodgram.settings import RECIPES_LIMIT
from recipes.models import Recipe

from .models import Follow

User = get_user_model()


class UserSerializerModified(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = ('email', 'username', 'id',
                  'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj).exists()


class MyAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email")
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                messsage = 'Неверные данные для входа.'
                raise serializers.ValidationError(messsage, code='authorization')
        else:
            message = 'Авторизация производится по паролю и email.'
            raise serializers.ValidationError(message, code='authorization')
        attrs['user'] = user
        return attrs


class ShowRecipeAddedSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = fields

    def get_image(self, obj):
        request = self.context.get('request')
        photo_url = obj.image.url
        return request.build_absolute_uri(photo_url)


class FollowRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShowFollowSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = fields

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return obj.follower.filter(user=obj, author=request.user).exists()

    def get_recipes(self, obj):
        recipes = obj.recipes.all()[:RECIPES_LIMIT]
        request = self.context.get('request')
        return ShowRecipeAddedSerializer(
            recipes,
            many=True,
            context={'request': request}
        ).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class FollowerRecipeSerializerDetails(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

    def get_image(self, obj):
        req = self.context['request']
        photo_url = obj.image.url
        return req.build_absolute_uri(photo_url)


class FollowSerializer(serializers.ModelSerializer):
    queryset = User.objects.all()
    user = serializers.PrimaryKeyRelatedField(queryset=queryset)
    author = serializers.PrimaryKeyRelatedField(queryset=queryset)

    class Meta:
        model = Follow
        fields = (
            'user',
            'author'
        )

    def validate(self, data):
        user = self.context.get('request').user
        author_id = data['author'].id
        follow_exist = Follow.objects.filter(
            user=user,
            author__id=author_id
        ).exists()

        if self.context.get('request').method == 'GET':
            if user.id == author_id or follow_exist:
                raise serializers.ValidationError(
                    'Подписка уже существует')

        if self.context.get('request').method == 'DELETE':
            if not follow_exist:
                raise serializers.ValidationError(
                    'Подписки не существует')
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShowFollowSerializer(
            instance.author,
            context=context).data
