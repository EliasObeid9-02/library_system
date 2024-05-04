from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model


from library_system.models import Book


class Review(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["book", "author"],
                name="unique_review_between_author_and_book",
            )
        ]

    STAR_COUNT_CHOICES = ((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"))

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="reviews"
    )
    stars = models.IntegerField(choices=STAR_COUNT_CHOICES)
    review = models.TextField()

    def __str__(self):
        return f"{self.author}: {self.book}"
