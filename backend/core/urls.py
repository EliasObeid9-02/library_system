from django.contrib import admin
from django.urls import path, include

api_patterns = [
    path("", include("user_auth.urls", namespace="user_auth")),
    path("", include("library_system.urls")),
]

urlpatterns = [
    path("api/", include(api_patterns)),
]
