from rest_framework import status
from rest_framework.permissions import BasePermission


class CanAccessPost(BasePermission):
    message = "You do not have permission to access this post."
    status_code = status.HTTP_404_NOT_FOUND

    def has_object_permission(self, request, view, obj):
        if (
            obj.author.isPublic
            or obj.author.check_for_friendship(request.user)
            or obj.author == request.user
        ):
            return True

        return False
