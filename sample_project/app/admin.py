from django.contrib import admin

from esia_auth.admin import ESIACompatibleUserAdmin

from .models import CustomUser


class UserAdmin(ESIACompatibleUserAdmin):
    pass


admin.site.register(CustomUser, UserAdmin)
