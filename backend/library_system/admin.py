from django.contrib import admin

from library_system import models


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Author's info",
            {
                "fields": ("first_name", "last_name"),
            },
        ),
    )


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Category name",
            {
                "fields": ("name",),
            },
        ),
    )


@admin.register(models.Publication)
class PublicationAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Publication name",
            {
                "fields": ("name",),
            },
        ),
    )


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Identification",
            {"fields": ("isbn",)},
        ),
        (
            "Details",
            {
                "fields": (
                    "authors",
                    "title",
                    "edition",
                    "publication",
                    "summary",
                    "pages",
                    "publish_date",
                ),
            },
        ),
        (
            "Categories and Language",
            {
                "fields": (
                    "categories",
                    "language",
                )
            },
        ),
    )
    list_display = (
        "display_title",
        "pages",
        "publish_date",
        "language",
        "isbn",
        "display_categories",
    )
    list_filter = ("authors", "categories", "isbn", "language")


@admin.register(models.BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Details",
            {
                "fields": (
                    "id",
                    "book",
                ),
            },
        ),
        (
            "Borrowing Details",
            {
                "fields": (
                    "borrower",
                    "due_date",
                    "status",
                )
            },
        ),
    )
    list_display = ("id", "display_book", "borrower", "due_date", "status")
    list_filter = ("book", "borrower", "status")
