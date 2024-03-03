from rest_framework.permissions import BasePermission


class CanAccessProfile(BasePermission):
    def has_object_permission(self, request, view, obj):
        if (
            obj.isPublic
            or obj.check_for_friendship(request.user)
            or obj == request.user
        ):
            return True

        return False
