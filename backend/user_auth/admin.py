from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user_auth.models import Player


@admin.register(Player)
class PlayerAdmin(UserAdmin):
    """
    Player model admin class.

    Allows for addition of new Player accounts
    or changing the data of old accounts
    """

    fieldsets = (
        (None, {"fields": ("username", "password", "date_joined")}),
        (("Personal info"), {"fields": ("nickname", "email")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "nickname", "email", "password1", "password2"),
            },
        ),
    )

    list_display = ("username", "nickname", "email")
    list_filter = ()

    readonly_fields = ("date_joined",)

    search_fields = ("username", "nickname")
    search_help_text = "Search for players by their username or nickname."
    ordering = ("date_joined",)
