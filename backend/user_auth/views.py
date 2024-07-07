from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
)

from knox.auth import TokenAuthentication
from knox.views import LoginView, LogoutView

from user_auth.models import ResetToken
from user_auth.serializers import (
    UserSerializer,
    EmailChangeSerializer,
    PasswordChangeSerializer,
    PasswordResetEmailSerializer,
    PasswordResetConfirmSerializer,
)
from user_auth.permissions import (
    AllowAny,
    IsAuthenticated,
    IsOwnerOrStaff,
)

UserModel = get_user_model()


class UserAuthViewSet(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
):
    authentication_classes = [TokenAuthentication]
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()

    def get_permissions(self):
        if self.action == "delete":
            permission_classes = [IsAuthenticated, IsOwnerOrStaff]
        else:
            permission_classes = [IsAuthenticated]
        return [perm() for perm in permission_classes]

    @action(methods=["post"], detail=False)
    def register(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return Response(
            {"Success": "user created successfully."},
            status=status.HTTP_201_CREATED,
        )

    @action(
        methods=["put", "patch"], detail=True, serializer_class=EmailChangeSerializer
    )
    def email_change(self, request, pk=None):
        user = self.get_object()
        serializer = self.serializer_class(
            instance=user,
            data=request.data,
            context={"user": user},
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["put", "patch"], detail=True, serializer_class=PasswordChangeSerializer
    )
    def password_change(self, request, pk=None):
        user = self.get_object()
        serializer = self.serializer_class(
            instance=user,
            data=request.data,
            context={"user": user},
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["post"],
        detail=False,
        permissions_classes=[AllowAny],
        serializer_class=PasswordResetEmailSerializer,
        queryset=ResetToken.objects.all(),
    )
    def password_reset_email(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = serializer.validated_data["email"]
        user = UserModel.objects.get(email=email)
        if user.send_password_reset_email():
            return Response(
                {"Success": "password reset email has been sent."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"Error": "password reset email already sent before. Retry later."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        methods=["post"],
        detail=True,
        serializer_class=PasswordResetConfirmSerializer,
        queryset=ResetToken.objects.all(),
    )
    def password_reset_confirm(self, request, pk=None):
        reset_token = self.get_object()
        user = reset_token.user

        if reset_token.is_expired:
            reset_token.delete()
            return Response(
                {"Error": "reset token is expired!"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = self.serializer_class(
            instance=user,
            data=request.data,
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        reset_token.delete()
        return Response(
            {"Success": "password reset success."},
            status=status.HTTP_200_OK,
        )
