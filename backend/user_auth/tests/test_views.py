import base64

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from knox.views import LogoutView
from knox.auth import AuthToken

User = get_user_model()

API_APP_NAME = "user_auth"

API_URL_NAMES = {
    "login": "auth-login",
    "logout": "auth-logout",
    "register": "auth-register",
    "list": "auth-list",
    "retrieve": "auth-detail",
    "update": "auth-detail",
    "delete": "auth-detail",
    "password-change": "auth-password-change",
}


def create_api_url(viewname, **kwargs):
    if viewname not in API_URL_NAMES:
        raise NotImplementedError({viewname: "this viewname is not included."})

    api_url_name = API_APP_NAME + ":" + API_URL_NAMES[viewname]
    url = reverse(api_url_name, kwargs=kwargs)
    return url


def get_basic_authorization_header(user):
    return (
        "Basic %s"
        % base64.b64encode(
            (f"{user.username}:{user.password}").encode("ascii")
        ).decode()
    )


def get_token_authorization_header(token):
    return "Token %s" % token


class UserAuthViewsTestCase(APITestCase):
    def setUp(self):
        """
        Sets up two unique users with their
        own tokens for API testing
        """

        self.main_user = User.objects.create_user(
            username="main_user",
            first_name="main_first_name",
            last_name="main_last_name",
            email="main_user@example.com",
            password="main_password",
        )
        self.main_user_password = "main_password"
        instance, self.main_token = AuthToken.objects.create(user=self.main_user)

        self.secondary_user = User.objects.create(
            username="secondary_user",
            first_name="secondary_first_name",
            last_name="secondary_last_name",
            email="secondary_user@example.com",
            password="secondary_password",
        )
        self.secondary_user_password = "secondary_password"
        instance, self.secondary_token = AuthToken.objects.create(
            user=self.secondary_user
        )

    def test_register_with_valid_data(self):
        data = {
            "username": "user",
            "first_name": "first",
            "last_name": "last",
            "email": "user@example.com",
            "password": "example123",
            "confirm_password": "example123",
        }

        url = create_api_url("register")
        response = self.client.post(url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg="test_register_valid_data incorrect status.",
        )
        self.assertTrue(
            "Success" in response.data,
            msg="test_register_valid_data incorrect return data.",
        )

    def test_register_with_existing_username(self):
        data = {
            "username": self.main_user.username,
            "first_name": self.main_user.first_name,
            "last_name": self.main_user.last_name,
            "email": self.main_user.email,
            "password": self.main_user_password,
            "confirm_password": self.main_user_password,
        }

        url = create_api_url("register")
        response = self.client.post(url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="register_existing_username incorrect status.",
        )
        self.assertTrue(
            "Fail" in response.data
            and "Errors" in response.data
            and "username" in response.data["Errors"],
            msg="register_existing_username incorrect return data.",
        )

    def test_register_with_invalid_password(self):
        data = {
            "username": "user",
            "first_name": "first",
            "last_name": "last",
            "email": "user@example.com",
            "password": "12345678",
            "confirm_password": "12345678",
        }

        url = create_api_url("register")
        response = self.client.post(url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="test_register_non_equal_passwords incorrect status.",
        )
        self.assertTrue(
            "Fail" in response.data
            and "Errors" in response.data
            and "password" in response.data["Errors"],
            msg="test_register_non_equal_passwords incorrect return data.",
        )

    def test_register_with_non_equal_passwords(self):
        data = {
            "username": "user",
            "first_name": "first",
            "last_name": "last",
            "email": "user@example.com",
            "password": "example123",
            "confirm_password": "12345678",
        }

        url = create_api_url("register")
        response = self.client.post(url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="test_register_non_equal_passwords incorrect status.",
        )
        self.assertTrue(
            "Fail" in response.data
            and "Errors" in response.data
            and "confirm_password" in response.data["Errors"],
            msg="test_register_non_equal_passwords incorrect return data.",
        )

    def test_update_with_valid_data(self):
        data = {
            "first_name": self.main_user.first_name,
            "email": self.main_user.email,
        }

        self.client.credentials(
            HTTP_AUTHORIZATION=get_token_authorization_header(self.main_token)
        )

        url = create_api_url("update", **{"pk": self.main_user.username})
        response = self.client.patch(url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg="test_update_with_owner incorrect status.",
        )
        self.assertTrue(
            "first_name" in response.data and "email" in response.data,
            msg="test_update_with_owner incorrect return data.",
        )

    def test_update_with_non_owner(self):
        data = {
            "first_name": self.main_user.first_name,
            "email": self.main_user.email,
        }

        self.client.credentials(
            HTTP_AUTHORIZATION=get_token_authorization_header(self.secondary_token)
        )

        url = create_api_url("update", **{"pk": self.main_user.username})
        response = self.client.patch(url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            msg="test_update_with_valid_data incorrect status.",
        )

    def test_delete_with_valid_data(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=get_token_authorization_header(self.main_token)
        )

        url = create_api_url("delete", **{"pk": self.main_user.username})
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            msg="test_delete_with_valid_data incorrect status.",
        )

    def test_delete_with_non_owner(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=get_token_authorization_header(self.secondary_token)
        )

        url = create_api_url("delete", **{"pk": self.main_user.username})
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            msg="test_delete_with_non_owner incorrect status.",
        )

    def test_password_change_with_valid_data(self):
        data = {
            "password": self.main_user_password,
            "new_password": self.secondary_user_password,
            "confirm_password": self.secondary_user_password,
        }

        self.client.credentials(
            HTTP_AUTHORIZATION=get_token_authorization_header(self.main_token)
        )

        url = create_api_url("password-change")
        response = self.client.patch(url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg="test_password_change_with_valid incorrect status.",
        )

    def test_password_change_with_incorrcet_old_password(self):
        data = {
            "password": self.secondary_user_password,
            "new_password": self.secondary_user_password,
            "confirm_password": self.secondary_user_password,
        }

        self.client.credentials(
            HTTP_AUTHORIZATION=get_token_authorization_header(self.main_token)
        )

        url = create_api_url("password-change")
        response = self.client.patch(url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="test_password_change_with_incorrcet_old_password incorrect status.",
        )
        self.assertTrue(
            "Errors" in response.data and "password" in response.data["Errors"],
            msg="test_password_change_with_incorrcet_old_password incorrect return data.",
        )

    def test_password_change_with_invalid_new_password(self):
        data = {
            "password": self.main_user_password,
            "new_password": 12345678,
            "confirm_password": 12345678,
        }

        self.client.credentials(
            HTTP_AUTHORIZATION=get_token_authorization_header(self.main_token)
        )

        url = create_api_url("password-change")
        response = self.client.patch(url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="test_password_change_with_invalid_new_password incorrect status.",
        )
        self.assertTrue(
            "Errors" in response.data and "new_password" in response.data["Errors"],
            msg="test_password_change_with_invalid_new_password incorrect return data.",
        )

    def test_password_change_with_non_equal_passwords(self):
        data = {
            "password": self.main_user_password,
            "new_password": self.secondary_user_password,
            "confirm_password": 12345678,
        }

        self.client.credentials(
            HTTP_AUTHORIZATION=get_token_authorization_header(self.main_token)
        )

        url = create_api_url("password-change")
        response = self.client.patch(url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="test_password_change_with_non_equal_passwords incorrect status.",
        )
        self.assertTrue(
            "Errors" in response.data and "confirm_password" in response.data["Errors"],
            msg="test_password_change_with_non_equal_passwords incorrect return data.",
        )
