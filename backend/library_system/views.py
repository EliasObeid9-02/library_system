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
    Book,
    BookInstance,
    Review,
)
from library_system.serializers import (
    AuthorSerializer,
    CategorySerializer,
    PublicationSerializer,
    BookSerializer,
    BookCreationSerializer,
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


class BookViewSet(
    GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
):
    authentication_classes = [TokenAuthentication]
    queryset = Book.objects.all()

    def get_permissions(self):
        if self.action in ("create", "update"):
            permission_classes = [IsAdminUser, IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [perm() for perm in permission_classes]

    def get_serializer_class(self):
        if self.action == "create":
            serializer_class = BookCreationSerializer
        else:
            serializer_class = BookSerializer
        return serializer_class


class ReviewViewSet(
    GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
