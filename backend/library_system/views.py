from rest_framework import permissions, authentication
from rest_framework.viewsets import ModelViewSet

from knox.auth import TokenAuthentication

from library_system import models, serializers


class GenericModelViewSet(ModelViewSet):
    # Authentication classes initialization
    authentication_classes = [authentication.BasicAuthentication]
    authentication_classes_mapping = {
        "PUT": [TokenAuthentication],
        "PATCH": [TokenAuthentication],
        "DELETE": [TokenAuthentication],
    }

    def get_authenticators(self):
        if not isinstance(self.authentication_classes_mapping, dict):
            raise ImproperlyConfigured(
                {
                    f"{self.__class__.__name__} get_authenticators": "authentication_classes_mapping must be a dict mapping."
                }
            )

        authentication_classes = self.authentication_classes
        if self.request.method in self.authentication_classes_mapping.keys():
            authentication_classes = self.authentication_classes_mapping[
                self.request.method
            ]
        return [auth() for auth in authentication_classes]

    # Permission classes initialization
    permission_classes = [permissions.AllowAny]
    permission_classes_mapping = {
        "PUT": [permissions.IsAuthenticated, permissions.IsAdminUser],
        "PATCH": [permissions.IsAuthenticated, permissions.IsAdminUser],
        "DELETE": [permissions.IsAuthenticated, permissions.IsAdminUser],
    }

    def get_permissions(self):
        if not isinstance(self.permission_classes_mapping, dict):
            raise ImproperlyConfigured(
                {
                    f"{self.__class__.__name__} get_permissions": "permission_classes_mapping must be a dict mapping."
                }
            )

        permission_classes = self.permission_classes
        if self.request.method in self.permission_classes_mapping.keys():
            permission_classes = self.permission_classes_mapping[self.request.method]
        return [perm() for perm in permission_classes]


class AuthorViewSet(GenericModelViewSet):
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer


class CategoryViewSet(GenericModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class PublicationViewSet(GenericModelViewSet):
    queryset = models.Publication.objects.all()
    serializer_class = serializers.PublicationSerializer


class BookViewSet(GenericModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer


class BookInstanceViewSet(GenericModelViewSet):
    queryset = models.BookInstance.objects.all()
    serializer_class = serializers.BookInstanceSerializer
