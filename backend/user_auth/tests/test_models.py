from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class UserAuthModelsTestCase(TestCase):
    def test_valid_nickname(self):
        user = User(
            username="user",
            nickname="user123-_",
            email="user@example.com",
            password="user_password",
        )

        try:
            user.full_clean()
        except:
            self.assertTrue(
                False,
                msg="test_valid_nickname user failed validation.",
            )

    def test_nickname_contains_special_characters(self):
        user = User(
            username="user",
            nickname="user123-_&",
            email="user@example.com",
            password="user_password",
        )

        with self.assertRaises(
            ValidationError,
            msg="test_nickname_contains_special_characters user didn't fail validation.",
        ):
            user.full_clean()
