from django.contrib import admin

from review_system import models


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Review detail",
            {
                "fields": (
                    "book",
                    "author",
                ),
            },
        ),
        (
            "Review",
            {
                "fields": (
                    "stars",
                    "review",
                )
            },
        ),
    )
