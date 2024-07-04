from django.db import models
from django.contrib.auth.models import AbstractUser

from user_auth.validators import validate_username, validate_email, validate_password


class User(AbstractUser):
    class Meta:
        indexes = [
            models.Index(
                fields=["username"],
                name="user_username_index",
            ),
            models.Index(
                fields=["email"],
                name="user_email_index",
            ),
        ]

    username = models.CharField(
        primary_key=True,
        max_length=150,
        validators=[validate_username],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )

    email = models.EmailField(
        unique=True,
        validators=[validate_email],
        error_messages={
            "unique": "A user with that email already exists",
        },
    )

    password = models.CharField(
        max_length=128,
        validators=[validate_password],
    )

    def promote(self):
        if self.is_staff:
            msg = "This user is already a staff member."
            return {"Error": msg}
        self.is_staff = True
        self.save()

        msg = "User promoted to staff member."
        return {"Success": msg}

    def demote(self):
        if self.is_superuser:
            msg = "This user is the main admin, can't demote."
            return {"Error": msg}

        if not self.is_staff:
            msg = "This user is not a staff member."
            return {"Error": msg}

        self.is_staff = False
        self.save()

        msg = "User demoted."
        return {"Success": msg}
