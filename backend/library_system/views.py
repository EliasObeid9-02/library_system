from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)

from knox.auth import TokenAuthentication

from library_system.permissions import IsOwnerOrStaff
from library_system.models import (
    Author,
    Category,
    Publication,
    Review,
)
from library_system.serializers import (
    AuthorSerializer,
    CategorySerializer,
    PublicationSerializer,
    ReviewSerializer,
)


class AuthorViewSet(
    GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


class CategoryViewSet(
    GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class PublicationViewSet(
    GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = PublicationSerializer
    queryset = Publication.objects.all()


class ReviewViewSet(
    GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
