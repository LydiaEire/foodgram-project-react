from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('admin/', admin.site.urls),
    path('api/', include('djoser.urls')),
    path('api/', include('recipes.urls')),
    path('api/', include('users.urls')),
]
