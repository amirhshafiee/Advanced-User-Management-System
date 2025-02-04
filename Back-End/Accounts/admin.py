from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'register_time', ]
    readonly_fields = ['register_time', ]
    fieldsets = (
        ("General info", {
            "fields": ("name", "email", "phone_number")
        }),
        ("Permissions", {
            "fields": ("is_admin", "is_staff", "is_superuser", "is_active",  'groups',
                'user_permissions')
        }),
        ("Important dates", {
            "fields": ("register_time", "last_login", )
        }),

    )