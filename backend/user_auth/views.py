from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured

from rest_framework import status, authentication
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.decorators import action

from knox.auth import TokenAuthentication
from knox.views import LoginView, LogoutView

from user_auth import serializers, permissions

User = get_user_model()


class UserAuthViewSet(GenericViewSet, ListAPIView, RetrieveUpdateDestroyAPIView):
    """
    The Authentication ViewSet, it provides the following methods
    get, list, update, login, register, password_change
    """

    queryset = User.objects.all()

    # Serializer class initialization
    serializer_class = serializers.EmptySerializer
    serializer_classes_mapping = {
        "list": serializers.UserSerializer,
        "retrieve": serializers.UserSerializer,
        "register": serializers.RegisterationSerializer,
        "destroy": serializers.UserSerializer,
        "update": serializers.UserSerializer,
        "partial_update": serializers.UserSerializer,
        "password_change": serializers.PasswordChangeSerializer,
    }

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes_mapping, dict):
            raise ImproperlyConfigured(
                {
                    "UserAuthViewSet get_serializer_class": "serializer_classes_mapping must be a dict mapping."
                }
            )

        if self.action not in self.serializer_classes_mapping.keys():
            raise ImproperlyConfigured(
                {
                    "UserAuthViewSet get_serializer_class": f"{self.action} not in serializer_classess_mapping."
                }
            )
        return self.serializer_classes_mapping[self.action]

    # Authentication classes initialization
    authentication_classes = [authentication.BasicAuthentication]
    authentication_classes_mapping = {
        "PUT": [TokenAuthentication],
        "PATCH": [TokenAuthentication],
        "DELETE": [TokenAuthentication],
    }

    def get_authenticators(self):
        if not isinstance(self.authentication_classes_mapping, dict):
            raise ImproperlyConfigured(
                {
                    "UserAuthViewSet get_authenticators": "authentication_classes_mapping must be a dict mapping."
                }
            )

        authentication_classes = self.authentication_classes
        if self.request.method in self.authentication_classes_mapping.keys():
            authentication_classes = self.authentication_classes_mapping[
                self.request.method
            ]
        return [auth() for auth in authentication_classes]

    # Permission classes initialization
    permission_classes = [permissions.AllowAny]
    permission_classes_mapping = {
        "PUT": [permissions.IsAuthenticated, permissions.IsOwner],
        "PATCH": [permissions.IsAuthenticated, permissions.IsOwner],
        "DELETE": [permissions.IsAuthenticated, permissions.IsOwner],
    }

    def get_permissions(self):
        if not isinstance(self.permission_classes_mapping, dict):
            raise ImproperlyConfigured(
                {
                    "UserAuthViewSet get_permissions": "permission_classes_mapping must be a dict mapping."
                }
            )

        permission_classes = self.permission_classes
        if self.request.method in self.permission_classes_mapping.keys():
            permission_classes = self.permission_classes_mapping[self.request.method]
        return [perm() for perm in permission_classes]

    # Main methods definition
    @action(methods=["POST"], detail=False)
    def register(self, request):
        """
        Registeration method that creates a new user
        """

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "Fail": "following data failed validation.",
                    "Errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return Response(
            {"Success": "new user created."},
            status=status.HTTP_201_CREATED,
        )

    @action(methods=["PUT", "PATCH"], detail=False)
    def password_change(self, request):
        """
        Password change method that allows the user to change their passwords
        """

        instance = self.request.user
        serializer = self.get_serializer(instance, data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "Fail": "following data failed validation",
                    "Errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return Response({"Success": "password changed."}, status=status.HTTP_200_OK)
