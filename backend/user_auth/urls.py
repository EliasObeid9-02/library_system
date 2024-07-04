from django.urls import path, include

from user_auth import views


auth_patterns = [
    path("login/", views.LoginView.as_view(), name="auth-login"),
    path("logout/", views.LogoutView.as_view(), name="auth-logout"),
]

urlpatterns = [
    path("auth/", include(auth_patterns)),
]
