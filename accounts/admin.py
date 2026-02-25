from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_staff',
                    'is_active', 'phone_number')
    list_filter = ('is_staff', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('phone_number', 'profile_picture')}),
        ('Permissions', {'fields': ('is_staff',
         'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2', 'is_staff', 'is_active', 'groups')}
         ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)
