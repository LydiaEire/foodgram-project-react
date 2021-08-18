import re

from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError
from rest_framework_simplejwt.serializers import PasswordField

from .models import FoodgramUser, Follow


class UserSerializer(serializers.ModelSerializer):
    """
    FoodgramUser serializer with 'is_subscribed' field
    """
    #role = serializers.CharField(required=False)

    username = serializers.CharField(
        max_length=64,
        min_length=5,
        allow_blank=False,
        trim_whitespace=True,
        validators=[UniqueValidator(queryset=FoodgramUser.objects.all())]
    )
    email = serializers.EmailField(
        min_length=5,
        validators=[UniqueValidator(queryset=FoodgramUser.objects.all())]
    )
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = FoodgramUser
        fields = [
            'username', 'first_name', 'last_name', 'email', 'is_subscribed', 'id',
        ]
        lookup_field = 'username'

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj).exists()


class EmailRegistrationSerializer(serializers.ModelSerializer):
    """
    FoodgramUser specific serializer for registration page
    """
    password = PasswordField(required=False)
    username_field = 'email'

    class Meta:
        model = FoodgramUser
        fields = ['email', 'password', ]


class UserVerificationSerializer(serializers.ModelSerializer):
    """
    FoodgramUser specific serializer for activation page
    """
    confirmation_code = serializers.CharField()
    email = serializers.EmailField(
        validators=[EmailValidator(), ]
    )

    class Meta:
        model = FoodgramUser
        fields = ['email', 'confirmation_code', ]

    def validate_confirmation_code(self, value):
        regex = r'\w{6}-\w{32}'
        if re.fullmatch(regex, value):
            return value
        raise ValidationError('The confirmation_code format is wrong')

