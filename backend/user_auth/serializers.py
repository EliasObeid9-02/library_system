from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import password_validation

from rest_framework import serializers
from rest_framework.validators import ValidationError

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("url", "username", "email", "password", "confirm_password")
        read_only_fields = ("url",)
        extra_kwargs = {
            "password": {"write_only": True},
        }

    confirm_password = serializers.CharField(max_length=128, write_only=True)

    def validate_password(self, password):
        password_validation.validate_password(password)
        return password

    def validate(self, validated_data):
        confirm_password = validated_data.pop("confirm_password")
        if validated_data["password"] != confirm_password:
            raise ValidationError({"confirm_password": "Passwords are not equal."})
        return validated_data


class PasswordChangeMixin(serializers.Serializer):
    new_password = serializers.CharField(max_length=128, write_only=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True)

    def validate_new_password(self, new_password):
        password_validation.validate_password(new_password)
        return new_password

    def validate(self, validated_data):
        new_password = validated_data.get("new_password")
        confirm_password = validated_data.get("confirm_password")
        if new_password != confirm_password:
            raise ValidationError({"confirm_password": "New passwords are not equal."})
        return validated_data

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance


class PasswordChangeSerializer(PasswordChangeMixin, serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("password", "new_password", "confirm_password")
        extra_kwargs = {
            "password": {"write_only": True},
            "new_password": {"write_only": True},
            "confirm_password": {"write_only": True},
        }

    def validate_password(self, password):
        user = self.context["user"]
        if not user or not user.check_password(password):
            raise ValidationError({"password": "Password is incorrect."})
        return password


class EmailChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("email", "password")
        write_only = ("email", "password")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_password(self, password):
        user = self.context["user"]
        if not user or not user.check_password(password):
            raise ValidationError({"password": "Password is incorrect."})
        return password

    def update(self, instance, validated_data):
        instance.email = validated_data["email"]
        instance.save()
        return instance


class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(
        write_only=True,
        required=True,
    )

    def validate_email(self, email):
        email = BaseUserManager.normalize_email(email)
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise ValidationError({"email": "No user with this email exists."})
        return email


class PasswordResetConfirmSerializer(PasswordChangeMixin, serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("new_password", "confirm_password")
