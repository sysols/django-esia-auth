from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class ESIACompatibleUserAdmin(UserAdmin):
    list_display = (
        'id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active',
    )
    search_fields = (
        'username', 'first_name', 'last_name', 'email',
    )
    list_filter = (
        'is_staff', 'is_active',
    )
    filter_horizontal = (
        'user_permissions', 'groups',
    )
