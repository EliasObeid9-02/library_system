from django.contrib import admin
from django.urls import path, include

api_patterns = [
    path("", include("user_auth.urls", namespace="user_auth")),
    path("", include("library_system.urls", namespace="library_system")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_patterns)),
]
