
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class DevHomesUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('DevHomes Info', {'fields': ('phone', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('DevHomes Info', {'fields': ('email', 'phone', 'role')}),
    )

    list_display = (
        'username',
        'email',
        'phone',
        'role',
        'is_staff',
        'is_superuser',
    )
    search_fields = ('username', 'email', 'phone')