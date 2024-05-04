from django.urls import path, include

from rest_framework.routers import DefaultRouter

from review_system import views

app_name = "review_system"

router = DefaultRouter()
router.register("", views.ReviewViewSet, basename="review")

urlpatterns = [
    path("reviews/", include(router.urls)),
]
