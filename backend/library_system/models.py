import uuid, datetime

from django.db import models
from django.db.models.functions import Lower
from django.contrib.auth import get_user_model

from library_system import utils
from library_system.validators import (
    NameValidator,
    ISBNValidator,
    MinValueValidator,
)


class Author(models.Model):
    """
    Book author, allows for filtering books by author
    """

    class Meta:
        # the tuple (first_name, last_name) is unique
        ordering = ["last_name", "first_name"]
        constraints = [
            models.UniqueConstraint(
                Lower("first_name"),
                Lower("last_name"),
                name="unique_author_name",
            )
        ]

    name_validator = NameValidator()

    first_name = models.CharField(max_length=40, validators=[name_validator])
    last_name = models.CharField(max_length=40, validators=[name_validator])

    def display_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.display_name()


class Category(models.Model):
    """
    Book category, allows for filtering books by category
    """

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        constraints = [
            models.UniqueConstraint(Lower("name"), name="unique_category_name")
        ]

    name_validator = NameValidator()

    name = models.CharField(
        primary_key=True, max_length=40, validators=[name_validator]
    )

    def save(self, *args, **kwargs):
        self.name = utils.capitalize_sentence(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Publication(models.Model):
    """
    Book publication, allows for filtering books by publication
    """

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("name"), name="unique_publication_name")
        ]

    name = models.CharField(primary_key=True, max_length=40)

    def save(self, *args, **kwargs):
        self.name = utils.capitalize_sentence(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Book(models.Model):
    class Meta:
        ordering = ["title", "-publish_date"]

    LANGUAGE_CHOICES = (
        ("en", "English"),
        ("zh", "Chinese"),
        ("de", "German"),
        ("es", "Spanish"),
        ("ja", "Japanese"),
        ("ru", "Russian"),
        ("ar", "Arabic"),
    )

    positive_integer_validator = MinValueValidator(
        limit_value=1, message="Value must be positive."
    )

    isbn = models.CharField(
        "ISBN",
        max_length=13,
        unique=True,
        validators=[ISBNValidator],
        help_text="13 character ISBN number.",
    )
    title = models.CharField(max_length=100)
    summary = models.TextField(help_text="A short summary of the book's story.")
    pages = models.IntegerField(default=1, validators=[positive_integer_validator])
    edition = models.IntegerField(
        default=1, blank=True, validators=[positive_integer_validator]
    )
    authors = models.ManyToManyField(Author, related_name="books")
    categories = models.ManyToManyField(Category, related_name="books")
    publication = models.ForeignKey(
        Publication, related_name="books", on_delete=models.RESTRICT
    )
    publish_date = models.DateField(default=datetime.date.today())
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default="en")

    def display_title(self):
        if self.edition is None:
            return f"{self.title}"
        return f"{self.title} [{utils.get_order(self.edition)} ed.]"

    def display_authors(self):
        return ", ".join([author.display_name() for author in self.authors.all()])

    def display_categories(self):
        return ", ".join([category.name for category in self.categories.all()])

    def __str__(self):
        return f"{self.display_title()} by {self.display_authors()}"


class BookInstance(models.Model):
    """
    A copy of a book available in the library.
    """

    class Meta:
        ordering = ["due_date"]

    BORROW_STATUS = (
        ("M", "Maintenance"),
        ("B", "Borrowed"),
        ("R", "Reserved"),
        ("A", "Available"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    borrower = models.ForeignKey(
        get_user_model(), on_delete=models.RESTRICT, null=True, blank=True
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date that the borrower must return the book by. Defaults to 3 weeks after borrowing.",
    )
    status = models.CharField(
        max_length=1, choices=BORROW_STATUS, blank=True, default="M"
    )

    @property
    def is_overdue(self):
        return self.due_date and due_date < datetime.date.today()

    def display_book(self):
        return self.book.display_title()

    def __str__(self):
        return f"{self.id} {self.book.title}"
