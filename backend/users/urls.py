from django.conf.urls import include
from django.urls import path, re_path

from .views import FollowViewSet, ListFollowViewSet

urlpatterns = [

    path(
        'users/subscriptions/',
        ListFollowViewSet,
        name='subscriptions'
    ),
    path(
        'users/<int:author_id>/subscribe/',
        FollowViewSet.as_view({'get': 'get', 'delete': 'delete'}),
        name='subscribe'
    ),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
