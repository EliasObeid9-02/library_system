from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    """
    User model admin class.

    Allows for addition of new User accounts
    or changing the data of old accounts
    """

    fieldsets = (
        (None, {"fields": ("username", "password", "date_joined")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "email")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    list_display = ("username", "first_name", "last_name", "email")
    list_filter = ()

    readonly_fields = ("date_joined",)

    search_fields = ("username",)
    search_help_text = "Search for players by their username."
    ordering = ("date_joined",)
