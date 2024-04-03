from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    SAFE_METHODS,
)


class ReadOnly(BasePermission):
    """
    Permission class that allows access only when the
    request method is safe (GET, HEAD or OPTIONS)
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsOwner(BasePermission):
    """
    Permission class that allows access only when the
    request user is the owner of object being viewed
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user
