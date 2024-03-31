from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator

from user_auth.validators import ASCIINicknameValidator


class Player(AbstractUser):
    """
    Replacement for the default User model in django

    Includes a modifible nickname that is displayed for the user
    """

    class Meta:
        verbose_name = "player"
        verbose_name_plural = "players"

    username_validator = ASCIIUsernameValidator()
    nickname_validator = ASCIINicknameValidator()

    username = models.CharField(
        max_length=150,
        primary_key=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    nickname = models.CharField(
        max_length=30,
        default="",
        help_text="Display name for your account.",
        validators=[nickname_validator],
    )
