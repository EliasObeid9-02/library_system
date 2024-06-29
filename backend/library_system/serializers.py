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


class BookCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = (
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
            "copies_count",
        )

    copies_count = serializers.IntegerField(default=0)

    def validate_copies_count(self, value):
        if value < 0:
            raise ValidationError(
                {"Book Creation": "copies count must be non negative."}
            )
        return value

    def create(self, validated_data):
        copies_count = validated_data.pop("copies_count")
        book_data = validated_data
        book = models.Book.objects.create(**book_data)
        book.save()

        instaces = [models.BookInstance(book=book) for _ in range(copies_count)]
        models.BookInstance.objects.bulk_create(instances)

        return book


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Review
        fields = ("url", "book", "reviewer", "stars", "review_text")
        read_only_fields = ("url",)
