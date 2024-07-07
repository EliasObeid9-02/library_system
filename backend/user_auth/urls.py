from django.urls import path, include

from rest_framework.routers import SimpleRouter

from user_auth import views

router = SimpleRouter()
router.register("", views.UserAuthViewSet, basename="user")

auth_patterns = [
    path("login/", views.LoginView.as_view(), name="user-login"),
    path("logout/", views.LogoutView.as_view(), name="user-logout"),
    path("", include(router.urls)),
]

urlpatterns = [
    path("auth/", include(auth_patterns)),
]
