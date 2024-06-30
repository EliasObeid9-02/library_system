import datetime

from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)

from knox.auth import TokenAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from library_system.filters import BookFilter
from library_system.permissions import IsOwnerOrStaff
from library_system.models import (
    Author,
    Category,
    Publication,
    Book,
    BookInstance,
    BookReservation,
    Review,
)
from library_system.serializers import (
    EmptySerializer,
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

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = BookFilter
    ordering_fields = ["pages", "publish_date", "reviews_star_average"]

    # def get_permissions(self):
    #     if self.action in ("create", "update"):
    #         permission_classes = [IsAdminUser, IsAuthenticated]
    #     else:
    #         permission_classes = [IsAuthenticated]
    #     return [perm() for perm in permission_classes]

    def get_serializer_class(self):
        if self.action == "create":
            serializer_class = BookCreationSerializer
        else:
            serializer_class = BookSerializer
        return serializer_class

    @action(methods=["post"], detail=True, serializer_class=EmptySerializer)
    def borrow_book(self, request, pk=None):
        book = Book.objects.get(pk=pk)
        user = request.user

        if BookInstance.objects.filter(book=book, borrower=user).exists():
            return Response(
                {"Error": "user already borrowed a copy of this book."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        available_books = BookInstance.available.filter(book=book)
        if available_books.count() > 0:
            instance = available_books.all()[0]
            instance.borrower = user
            instance.due_date = datetime.datetime.now() + datetime.timedelta(days=21)
            instance.status = "B"
            instance.save()
            return Response(
                {"Success": "user has borrowed a copy of this book."},
                status=status.HTTP_200_OK,
            )

        if BookReservation.objects.filter(book=book, borrower=user).exists():
            return Response(
                {"Error": "user has already placed a reservation on this book."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reservation = BookReservation(book=book, borrower=user)
        reservation.save()
        return Response(
            {"Success": "user has placed a reservation order on this book."},
            status=status.HTTP_201_CREATED,
        )

    @action(methods=["post"], detail=True, serializer_class=EmptySerializer)
    def return_book(self, request, pk=None):
        book = self.get_object()
        user = request.user

        if not BookInstance.objects.filter(book=book, borrower=user).exists():
            return Response(
                {"Error": "user hasn't borrowed a copy of this book."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reservations = book.reservations
        instance = BookInstance.objects.filter(book=book, borrower=user)[0]
        if reservations.count() > 0:
            first_reservation = reservations[0]
            instance.borrower = first_reservation.borrower
            instance.due_date = datetime.datetime.now() + datetime.timedelta(days=21)
            first_reservation.delete()
        else:
            instance.borrower = None
            instance.due_date = None
            instance.status = "A"
        instance.save()

        return Response(
            {"Success": "user returned the borrowed copy of the book."},
            status=status.HTTP_200_OK,
        )


class ReviewViewSet(
    GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
