from rest_framework import serializers

from user_auth.serializers import UserSerializer
from library_system.serializers import BookSerializer
from review_system.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Review
