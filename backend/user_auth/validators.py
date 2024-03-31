import re

from django.core.validators import RegexValidator


class ASCIINicknameValidator(RegexValidator):
    regex = r"^[\w\d-]+\Z$"
    message = "Nickname must be composed of English letters, \
               numbers, hyphens and underscores only."
    flags = re.ASCII
