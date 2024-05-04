from rest_framework import serializers

from library_system import models
from user_auth.serializers import UserSerializer


class EmptySerializer(serializers.Serializer):
    pass


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Author


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Category


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Publication


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Book


class BookInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.BookInstance
