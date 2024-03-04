from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission


class CustomForbidden(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "You dont have access to view this post."


class CanAccessPost(BasePermission):
    def has_object_permission(self, request, view, obj):
        if (
            obj.author.isPublic
            or obj.author.check_for_friendship(request.user)
            or obj.author == request.user
        ):
            return True

        raise CustomForbidden


class CanAccessFeed(BasePermission):
    message = "You do not have permission to access this feed."
    status_code = status.HTTP_404_NOT_FOUND

    def has_object_permission(self, request, view, obj):
        if (
            obj.isPublic
            or obj.check_for_friendship(request.user)
            or obj == request.user
        ):
            return True

        raise CustomForbidden
