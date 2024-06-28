from django.urls import path, include

from rest_framework.routers import SimpleRouter

from library_system import apps
from library_system.views import (
    AuthorViewSet,
    CategoryViewSet,
    PublicationViewSet,
    ReviewViewSet,
)


router = SimpleRouter()
router.register("author", AuthorViewSet, basename="author")
router.register("category", CategoryViewSet, basename="category")
router.register("publication", PublicationViewSet, basename="publication")
router.register("review", ReviewViewSet, basename="review")

urlpatterns = [
    path("library_system/", include(router.urls)),
]
