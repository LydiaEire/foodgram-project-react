import re

from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError
from rest_framework_simplejwt.serializers import PasswordField

from backend.users.models import FoodgramUser


class UserSerializer(serializers.ModelSerializer):
    """
    Default FoodgramUser serializer
    """
    role = serializers.CharField(required=False)

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

    class Meta:
        model = FoodgramUser
        fields = [
            'username', 'first_name', 'last_name', 'email', 'bio', 'role',
        ]
        lookup_field = 'username'


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