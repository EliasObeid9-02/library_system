import datetime

from django.db import models
from django.db.models.functions import Lower
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model

from library_system.apps import app_name
from library_system.validators import (
    name_validator,
    isbn_validator,
    positive_value_validator,
)


user_model = get_user_model()


def get_order(value: int):
    if value % 10 == 1:
        return f"{value}st."
    elif value % 10 == 2:
        return f"{value}nd."
    elif value % 10 == 3:
        return f"{value}rd."
    else:
        return f"{value}th."


class SlugMixin:
    def create_slug(self):
        raise NotImplementedError(
            {f"Class {type(self).__name__}": "create_slug not implemented."}
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = self.create_slug()
            self.save()


class Author(SlugMixin, models.Model):
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

    slug = models.SlugField(
        max_length=100,
        unique=True,
        null=False,
    )

    def create_slug(self):
        text = f"{self.first_name} {self.last_name}_{self.id}"
        return slugify(text)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Category(SlugMixin, models.Model):
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

    slug = models.SlugField(
        max_length=60,
        unique=True,
        null=False,
    )

    def create_slug(self):
        text = f"{self.name}_{self.id}"
        return slugify(text)

    def __str__(self):
        return self.name


class Publication(SlugMixin, models.Model):
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

    slug = models.SlugField(
        max_length=60,
        unique=True,
        null=False,
    )

    def create_slug(self):
        text = f"{self.name}_{self.id}"
        return slugify(text)

    def __str__(self):
        return self.name


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

    @property
    def full_title(self):
        if self.edition:
            return f"{self.title} [{get_order(self.edition)}]"
        return self.title

    def __str__(self):
        return self.full_title


class AvailableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="A")


class BorrowedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="B")


class BookInstance(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                "book",
                "borrower",
                name="book_instance_unique_book_borrower",
            )
        ]

        indexes = [
            models.Index(
                fields=["status", "book"],
                name="b-instance_status_book_index",
            ),
            models.Index(
                fields=["book", "borrower"],
                name="b-instance_book_borrower_index",
            ),
        ]

    objects = models.Manager()
    available = AvailableManager()
    borrowed = BorrowedManager()

    BORROW_STATUS = (
        ("A", "Available"),
        ("B", "Borrowed"),
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
        default="A",
    )

    @property
    def is_overdue(self):
        return self.due_date and due_date < datetime.date.today()

    def __str__(self):
        return f"{self.book} borrowed by {self.borrower}"


class BookReservation(models.Model):
    class Meta:
        indexes = [
            models.Index(
                fields=["id", "book"],
                name="b-reservation_id_book",
            ),
        ]

    book = models.ForeignKey(
        to="Book",
        on_delete=models.CASCADE,
        related_name="reservations",
    )

    borrower = models.ForeignKey(
        to=user_model,
        on_delete=models.CASCADE,
        related_name="reservations",
    )

    def __str__(self):
        return f"{self.book} to be borrowed by {self.borrower}"


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
        choices=models.IntegerChoices("Stars", "1 2 3 4 5").choices,
    )

    review_text = models.TextField(
        help_text="Write your review here.",
    )

    def __str__(self):
        return f"{self.book} reviewed by {self.reviewer}"
