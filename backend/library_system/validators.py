import re

from django.core.validators import RegexValidator, MinValueValidator


class NameValidator(RegexValidator):
    regex = r"[A-Z\s\.]+"
    message = "Name must consist of only letters."
    flags = re.IGNORECASE


class ISBNValidator(RegexValidator):
    regex = r"[\d]{13}"
    message = "ISBN must be a string of digits of length 13."
