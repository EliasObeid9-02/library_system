from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.backends import BaseBackend

UserModel = get_user_model()


class UsernameBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        if not username or not password:
            return

        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password):
                return user


class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        if not email or not password:
            return

        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password):
                return user
