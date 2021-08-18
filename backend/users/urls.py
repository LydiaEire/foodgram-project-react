from django.conf.urls import include
from django.urls import path, re_path

from .views import RegistrUserView

urlpatterns = [
    #path('api-auth', include('rest_framework.urls')),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
