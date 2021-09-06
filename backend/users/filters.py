from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from .models import Follow

User = get_user_model()


class FollowFilter(filters.FilterSet):
    is_subscribed = filters.BooleanFilter(method='get_is_subscribed')

    class Meta:
        model = Follow
        fields = ['is_subscribed']

    def get_is_subscribed(self, queryset, value, is_subscribed):
        user = self.request.user
        if not user.is_authenticated:
            return queryset
        if is_subscribed:
            return queryset.filter(
                user=self.request.user
            ).distinct()
        return queryset
