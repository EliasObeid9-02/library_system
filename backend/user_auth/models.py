from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator


class User(AbstractUser):
    """
    Replacement for the default User model in django

    Includes a modifible nickname that is displayed for the user
    """

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    username_validator = ASCIIUsernameValidator()

    username = models.CharField(
        max_length=150,
        primary_key=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )

    def __str__(self):
        return f"{self.username} - {self.first_name} {self.last_name}"
