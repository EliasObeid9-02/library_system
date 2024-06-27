from rest_framework import serializers
from rest_framework.validators import ValidationError

from library_system import models


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = ("url", "slug", "full_name", "first_name", "last_name")
        read_only_fields = ("url", "slug", "full_name")
        write_only_fields = ("first_name", "last_name")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ("url", "slug", "name")
        read_only_fields = ("url", "slug")


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Publication
        fields = ("url", "slug", "name")
        read_only_fields = ("url", "slug")


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Book
        fields = (
            "url",
            "full_tile",
            "reviews_star_average",
            "title",
            "edition",
            "isbn",
            "summary",
            "pages",
            "authors",
            "categories",
            "publication",
            "publish_date",
            "language",
        )
        read_only_fields = ("url", "full_title", "reviews_star_average")
        write_only_fields = ("title", "edition")


class BookInstanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.BookInstance
        fields = ("url", "is_overdue", "book", "borrower", "due_date", "status")
        read_only_fields = ("url", "is_overdue")

    def validate_book(self, value):
        if self.instance is not None:
            raise ValidationError({"book": "this field is not updatable."})
        return value


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Review
        fields = ("url", "book", "reviewer", "stars", "review_text")
        read_only_fields = ("url",)
