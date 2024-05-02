from django.urls import path, include

from rest_framework.routers import DefaultRouter

from library_system import views

app_name = "library_system"


router = DefaultRouter()
router.register("author", views.AuthorViewSet, basename="author")
router.register("category", views.CategoryViewSet, basename="category")
router.register("publication", views.PublicationViewSet, basename="publication")
router.register("book", views.BookViewSet, basename="book")
router.register("book_instance", views.BookInstanceViewSet, basename="book_instance")

urlpatterns = [
    path("library/", include(router.urls)),
]
