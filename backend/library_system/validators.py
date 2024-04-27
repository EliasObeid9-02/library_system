import re

from django.core.validators import RegexValidator


class NameValidator(RegexValidator):
    regex = r"[A-Z]+"
    message = "Name must consist of only letters."
    flags = re.IGNORECASE


class ISBNValidator(RegexValidator):
    regex = r"[\d]{13}"
    message = "ISBN must be a string of digits of length 13."
