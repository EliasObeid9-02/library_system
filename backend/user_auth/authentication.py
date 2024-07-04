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

        auth_type, userid, password = auth_decoded.split(":", 2)
    except:
        msg = "Invalid basic header. Credentials not correctly base64 encoded."
        return {"Error": msg}
    return {"Success": (auth_type, userid, password)}


class AuthenticationMixin:
    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b"basic":
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


class UsernameAuthentication(AuthenticationMixin, BasicAuthentication):
    def authenticate(self, request):
        ret = super().authenticate(request)
        auth_type, username, password = ret

        if auth_type.lower() != "username":
            return None

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
    def authenticate(self, request):
        ret = super().authenticate(request)
        auth_type, email, password = ret

        if auth_type.lower() != "email":
            return None

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
