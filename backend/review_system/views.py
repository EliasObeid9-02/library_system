from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from knox.auth import TokenAuthentication

from review_system import models, serializers


class ReviewViewSet(ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
