import base64

from django.contrib.auth import get_user_model, authenticate

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BasicAuthentication, get_authorization_header

UserModel = get_user_model()


def decode_auth_header(auth_header: str):
    try:
        try:
            auth_decoded = base64.b64decode(auth_header).decode("utf-8")
        except UnicodeDecodeError:
            auth_decoded = base64.b64decode(auth_header).decode("latin-1")

        userid, password = auth_decoded.split(":", 1)
    except:
        msg = "Invalid header. Credentials not correctly base64 encoded."
        return {"Error": msg}
    return {"Success": (userid, password)}


class AuthenticationMixin:
    auth_type = b""

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.auth_type:
            return None

        if len(auth) == 1:
            msg = "Invalid basic header. No credentials provided."
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = "Invalid basic header. Credentials string should not contain spaces."
            raise AuthenticationFailed(msg)

        ret = decode_auth_header(auth[1])
        if ret.get("Error"):
            msg = ret[1]
            raise AuthenticationFailed(msg)
        return ret["Success"]

    def get_auth_type(self):
        return self.auth_type.decode("utf-8").capitalize()

    def authenticate_header(self, request):
        return f"{self.get_auth_type()} realm={self.www_authenticate_realm}"


class UsernameAuthentication(AuthenticationMixin, BasicAuthentication):
    auth_type = b"username"

    def authenticate(self, request):
        ret = super().authenticate(request)
        if ret is None:
            return None

        username, password = ret
        return self.authenticate_credentials(username, password, request)

    def authenticate_credentials(self, username, password, request=None):
        credentials = {
            UserModel.USERNAME_FIELD: username,
            "password": password,
        }
        user = authenticate(request=request, **credentials)

        if user is None:
            raise AuthenticationFailed("Invalid username/password.")

        if not user.is_active:
            raise AuthenticationFailed("User inactive or deleted.")

        return (user, None)


class EmailAuthentication(AuthenticationMixin, BasicAuthentication):
    auth_type = b"email"

    def authenticate(self, request):
        ret = super().authenticate(request)
        if ret is None:
            return None

        email, password = ret
        return self.authenticate_credentials(email, password, request)

    def authenticate_credentials(self, email, password, request=None):
        credentials = {
            UserModel.EMAIL_FIELD: email,
            "password": password,
        }
        user = authenticate(request=request, **credentials)

        if user is None:
            raise AuthenticationFailed("Invalid email/password.")

        if not user.is_active:
            raise AuthenticationFailed("User inactive or deleted.")

        return (user, None)
