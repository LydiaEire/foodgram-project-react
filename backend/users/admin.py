from django.contrib import admin

from .models import FoodgramUser, Follow


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email',
                    'first_name', 'last_name', 'is_staff']
    list_filter = ['email', 'username']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ['username']
    ordering = ['email']
    filter_horizontal = ()


class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author', 'created_at')
    list_filter = ('created_at',)


admin.site.register(FoodgramUser, UserAdmin)
admin.site.register(Follow, FollowAdmin)
