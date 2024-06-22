import datetime

from django.db import models
from django.db.models.functions import Lower
from django.contrib.auth import get_user_model

from library_system.apps import app_name
from library_system.validators import (
    name_validator,
    isbn_validator,
    positive_value_validator,
)

user_model = get_user_model()


class Author(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("first_name"),
                Lower("last_name"),
                name="author_unique_full_name",
            )
        ]

        indexes = [
            models.Index(
                fields=["first_name", "last_name"],
                name="author_full_name_index",
            ),
        ]

    first_name = models.CharField(
        max_length=40,
        validators=[name_validator],
    )

    last_name = models.CharField(
        max_length=40,
        validators=[name_validator],
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse(f"{app_name}:author-detail", kwargs={"pk": self.pk})


class Category(models.Model):
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="category_unique_name",
            )
        ]

        indexes = [
            models.Index(
                fields=["name"],
                name="category_name_index",
            ),
        ]

    name = models.CharField(
        max_length=40,
        validators=[name_validator],
    )

    def get_absolute_url(self):
        return reverse(f"{app_name}:category-detail", kwargs={"pk": self.pk})


class Publication(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="publication_unique_name",
            ),
        ]

        indexes = [
            models.Index(
                fields=["name"],
                name="publication_name_index",
            ),
        ]

    name = models.CharField(
        max_length=40,
    )

    def get_absolute_url(self):
        return reverse(f"{app_name}:publication-detail", kwargs={"pk": self.pk})


class Book(models.Model):
    class Meta:
        indexes = [
            models.Index(
                fields=["language"],
                name="book_language_index",
            ),
        ]

    LANGUAGE_CHOICES = (
        ("en", "English"),
        ("zh", "Chinese"),
        ("de", "German"),
        ("es", "Spanish"),
        ("ja", "Japanese"),
        ("ru", "Russian"),
        ("ar", "Arabic"),
    )

    isbn = models.CharField(
        verbose_name="ISBN",
        max_length=13,
        unique=True,
        validators=[isbn_validator],
        help_text="13 character ISBN number.",
    )

    title = models.CharField(
        max_length=100,
    )

    summary = models.TextField(
        help_text="A short summary of the book's story.",
    )

    pages = models.IntegerField(
        null=True,
        blank=True,
        validators=[positive_value_validator],
    )

    edition = models.IntegerField(
        null=True,
        blank=True,
        validators=[positive_value_validator],
    )

    authors = models.ManyToManyField(
        to="Author",
        related_name="books",
    )

    categories = models.ManyToManyField(
        to="Category",
        related_name="books",
    )

    publication = models.ForeignKey(
        to="Publication",
        on_delete=models.PROTECT,
        related_name="books",
    )

    publish_date = models.DateField(
        null=True,
        blank=True,
    )

    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default="en",
    )

    @property
    def reviews_star_average(self):
        stars_average = self.reviews.aggregate(models.Avg("stars", default=0))
        return stars_average["stars__avg"]

    def get_absolute_url(self):
        return reverse(f"{app_name}:book-detail", kwargs={"pk": self.pk})


class BookInstance(models.Model):
    class Meta:
        indexes = [
            models.Index(
                fields=["due_date"],
                name="book_instance_due_date_index",
            ),
        ]

    BORROW_STATUS = (
        ("M", "Maintenance"),
        ("B", "Borrowed"),
        ("R", "Reserved"),
        ("A", "Available"),
    )

    book = models.ForeignKey(
        to="Book",
        on_delete=models.CASCADE,
        related_name="book_copies",
    )

    borrower = models.ForeignKey(
        to=user_model,
        on_delete=models.RESTRICT,
        related_name="borrowed_books",
        null=True,
        blank=True,
    )

    due_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date that the borrower must return the book by. Defaults to 3 weeks after borrowing.",
    )

    status = models.CharField(
        max_length=1,
        choices=BORROW_STATUS,
        blank=True,
        default="M",
    )

    @property
    def is_overdue(self):
        return self.due_date and due_date < datetime.date.today()

    def get_absolute_url(self):
        return reverse(f"{app_name}:book_instance-detail", kwargs={"pk": self.pk})


class Review(models.Model):
    class Meta:
        indexes = [
            models.Index(
                fields=["book", "stars"],
                name="review_book_stars_index",
            ),
        ]

    book = models.ForeignKey(
        to="Book",
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    reviewer = models.ForeignKey(
        to=user_model,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    stars = models.IntegerField(
        choices=models.IntegerChoices("Stars", "ONE TWO THREE FOUR FIVE").choices,
    )

    review_text = models.TextField(
        help_text="Write your review here.",
    )

    def get_absolute_url(self):
        return reverse(f"{app_name}:review-detail", kwargs={"pk": self.pk})
