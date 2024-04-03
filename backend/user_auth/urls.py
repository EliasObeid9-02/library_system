from django.urls import path, include

from rest_framework.routers import DefaultRouter

from user_auth import views

app_name = "user_auth"

router = DefaultRouter()
router.register("", views.UserAuthViewSet, basename="auth")

auth_patterns = [
    path("login/", views.LoginView.as_view(), name="auth-login"),
    path("logout/", views.LogoutView.as_view(), name="auth-logout"),
    path("", include(router.urls)),
]

urlpatterns = [
    path("auth/", include(auth_patterns)),
]
