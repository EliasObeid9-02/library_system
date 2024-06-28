from rest_framework.permissions import BasePermission


class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        if bool(
            request.user and (request.user.is_staff or request.user == obj.reviewer)
        ):
            return True
        return False
