from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

User = get_user_model()


class EmptySerializer(serializers.Serializer):
    """
    An empty serializer for use in the UserAuthViewSet
    """

    pass


class UserSerializer(serializers.ModelSerializer):
    """
    The player class serializer, returns the player's username, nickname and email
    """

    class Meta:
        fields = ("username", "nickname", "email")
        read_only = ("username",)
        model = User

    def create(self, data):
        raise NotImplementedError(
            {"UserSerializer": "create method not allowed with this serializer."}
        )


class RegisterationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "nickname", "email", "password", "confirm_password")
        write_only = ("password",)
        model = User

    confirm_password = serializers.CharField(max_length=150, write_only=True)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "username already exists."})
        return username

    def validate_email(self, email):
        # TODO: implement unique email check for the User model and Serializer
        return BaseUserManager.normalize_email(email)

    def validate_password(self, password):
        password_validation.validate_password(password)
        return password

    def validate(self, data):
        password = data["password"]
        confirm_password = data.pop("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "passwords are not equal."}
            )
        data["password"] = make_password(password)
        return data

    def update(self, instance, data):
        raise NotImplementedError(
            {
                "ReigsterationSerializer": "update method not allowed with this serializer."
            }
        )


class PasswordChangeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("password", "new_password", "confirm_password")
        write_only = ("password",)
        model = User

    new_password = serializers.CharField(max_length=150, write_only=True)
    confirm_password = serializers.CharField(max_length=150, write_only=True)

    def validate_password(self, password):
        user = self.context["request"].user
        if not user.check_password(password):
            raise serializers.ValidationError({"password": "incorrect password."})
        return password

    def validate_new_password(self, new_password):
        password_validation.validate_password(new_password)
        return new_password

    def validate(self, data):
        new_password = data.pop("new_password")
        confirm_password = data.pop("confirm_password")

        if new_password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "new passwords do not match."}
            )
        data["password"] = new_password
        return data

    def create(self, data):
        raise NotImplementedError(
            {
                "ChangePasswordSerializer": "create method not allowed with this serializer."
            }
        )

    def update(self, instance, data):
        instance.set_password(data["password"])
        instance.save()
        return instance
