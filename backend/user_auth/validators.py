from django.core.validators import ValidationError
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.auth.password_validation import validate_password

username_validator = ASCIIUsernameValidator()


def validate_username(username):
    return username_validator(username)


def validate_email(email):
    return BaseUserManager.normalize_email(email)
