from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FoodgramUser, Follow
from .serializers import FollowSerializer, ShowFollowSerializer

User = get_user_model()


class ListFollowViewSet(generics.ListAPIView):
    queryset = FoodgramUser.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = ShowFollowSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_queryset(self):
        user = self.request.user
        return FoodgramUser.objects.filter(following__user=user)


class FollowViewSet(APIView):
    """
    APIView with post and delete options.
    Used to create and delete Follow objects.
    """
    permission_classes = [IsAuthenticated, ]

    def get(self, request, author_id):
        user = request.user
        follow_exist = Follow.objects.filter(
            user=user,
            author__id=author_id
        ).exists()
        if user.id == author_id or follow_exist:
            return Response(
                {"Fail": "Ошибка"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'user': user.id,
            'author': author_id
        }
        serializer = FollowSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, author_id):
        obj = get_object_or_404(Follow, user=request.user, author=author_id)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
