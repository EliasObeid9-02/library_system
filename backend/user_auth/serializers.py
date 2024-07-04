from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import ValidationError

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("url", "username", "email", "password", "confirm_password")
        read_only = ("url",)
        write_only = ("password", "confirm_password")

    confirm_password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, validated_data):
        confirm_password = validated_data.pop("confirm_password")
        if validated_data["password"] != confirm_password:
            raise ValidationError({"confirm_password": "Passwords are not equal."})
        return validated_data


class PasswordChangeMixin:
    new_password = serializers.CharField(max_length=128, write_only=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True)

    def validate_new_password(self, value):
        if not validate_password(value):
            raise ValidationError({"new_password": "New password is too weak."})
        return value

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
        write_only = ("password", "new_password", "confirm_password")

    def validate_password(self, value):
        user = self.context["request"].user
        if not user or not user.check_password(value):
            raise ValidationError({"password": "Password is incorrect."})
        return value


class EmailChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("email", "password")
        write_only = ("email", "password")

    def validate_password(self, value):
        user = self.context["request"].user
        if not user or not user.check_password(value):
            raise ValidationError({"password": "Password is incorrect."})
        return value

    def update(self, instance, validated_data):
        instance.email = validated_data["email"]
        instance.save()
        return instance


class EmailPasswordReset(serializers.Serializer):
    email = serializers.EmailField(
        write_only=True,
        required=True,
    )

    def validate_email(self, value):
        value = BaseUserManager.normalize_email(value)
        try:
            user = UserModel.objects.get(email=value)
        except UserModel.DoesNotExist:
            raise ValidationError({"email": "No user with this email exists."})
        return value


class PasswordReset(PasswordChangeMixin, serializers.ModelSerializer):
    class Meta:
        fields = ("new_password", "confirm_password")
        write_only = ("new_password", "confirm_password")
