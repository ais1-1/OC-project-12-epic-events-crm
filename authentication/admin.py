from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    """Custom user admin"""

    list_display = (
        "last_name",
        "first_name",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "role",
    )
    ordering = (
        "last_name",
        "first_name",
    )
    search_fields = ("last_name", "first_name", "email")

    fieldsets = (
        # Authentication fields - email and password
        (None, {"fields": ("email", "password")}),
        ("Personal information", {"fields": ("last_name", "first_name", "role")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "joined_date")}),
    )

    add_fieldsets = (
        # Section pour les champs lors de l'ajout d'un nouvel utilisateur
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "last_name",
                    "first_name",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "role",
                    "joined_date",
                ),
            },
        ),
    )


admin.site.register(User, UserAdmin)
