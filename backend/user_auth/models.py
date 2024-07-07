import os
import binascii

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser

from user_auth.validators import validate_username, validate_email, validate_password
from core.settings import RESET_TOKEN_SETTINGS, HOST_SETTINGS


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

    def send_password_reset_email(self):
        reset_token, created = ResetToken.objects.get_or_create(user=self)
        if not created or reset_token.is_expired:
            return False

        url = reverse("user-password-reset-confirm", args=[reset_token.reset_token])
        subject = f"Password Reset Email"
        message = f"Hello,\n\n\
        We've received a password reset request for this email. Here is the link to reset the password:\n\n\
        {HOST_SETTINGS.get("protocol")}://{HOST_SETTINGS.get("domain")}{url}"
        send_mail(
            subject=subject,
            from_email=None,
            message=message,
            recipient_list=[self.email],
        )
        return True


class ResetToken(models.Model):
    class Meta:
        verbose_name = "Reset Token"
        db_table = "reset_token"

        indexes = [
            models.Index(fields=["user"], name="reset_token_user_index"),
        ]

    reset_token = models.CharField(
        max_length=40,
        primary_key=True,
    )

    user = models.OneToOneField(
        to=User,
        unique=True,
        on_delete=models.CASCADE,
        related_name="reset_token",
    )

    expire_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.reset_token:
            self.reset_token = self.generate_token()

        if not self.expire_time:
            self.expire_time = self.generate_expire_time()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_token(cls):
        return binascii.hexlify(os.urandom(RESET_TOKEN_SETTINGS.get("token_length"))).decode()

    @classmethod
    def generate_expire_time(cls):
        current_time = timezone.now()
        expire_time = current_time + RESET_TOKEN_SETTINGS.get("expiration_time")
        return expire_time

    @property
    def is_expired(self):
        current_time = timezone.now()
        return self.expire_time < current_time
