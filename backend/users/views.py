from uuid import uuid1

from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import FoodgramUser
from users.permissions import IsAdmin
from users.serializers import (
    UserSerializer, EmailRegistrationSerializer, UserVerificationSerializer)


class CreateUser(generics.CreateAPIView):
    """
    Create user with POST request with email parameter.
    Wait for email confirmation code.
    """
    permission_classes = (AllowAny, )
    serializer_class = EmailRegistrationSerializer

    def perform_create(self, serializer):
        serializer.save(
            is_active=False,
            password=make_password(None),
            username=str(uuid1()),
        )


class ConfirmUser(generics.UpdateAPIView):
    """
    Activate your user with POST request included email
    and confirmation_code params
    """
    serializer_class = UserVerificationSerializer
    permission_classes = (AllowAny, )
    http_method_names = ['post', ]

    def get_object(self):
        return get_object_or_404(
            FoodgramUser, email=self.request.data.get('email')
        )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'Error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/json',
            )
        user = self.get_object()
        code = request.data.get('confirmation_code')

        user.is_active = True
        user.save()
        check = default_token_generator.check_token(user, code)
        if not check:
            return Response(
                {'Error': 'Confirmation code for this email is wrong'},
                status=status.HTTP_401_UNAUTHORIZED,
                content_type='application/json',
            )
        token = AccessToken.for_user(user)
        return Response(
            data={'token': str(token)},
            status=status.HTTP_202_ACCEPTED,
            content_type='application/json',
        )


class UsersViewSet(viewsets.ViewSetMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   generics.GenericAPIView,):
    """
    Users List (for admins only), Send PATCH request to /api/v1/users/me/
    for editing your own profile.
    """
    queryset = FoodgramUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsYamdbAdmin, )

    @action(methods=['get', 'patch'], detail=False,
            permission_classes=[IsAuthenticated, ],
            url_path='me', url_name='personal_data')
    def personal_data(self, request):
        if request.method == 'GET':
            me = request.user
            serializer = self.get_serializer(me)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
                content_type='application/json',
            )
        if request.method == 'PATCH':
            me = request.user
            serializer = self.get_serializer(
                me, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
                content_type='application/json',
            )

