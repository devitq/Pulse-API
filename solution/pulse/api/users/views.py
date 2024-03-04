from datetime import timedelta

import bcrypt
import jwt
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.exceptions import (
    NotAuthenticated,
    NotFound,
    PermissionDenied,
    ValidationError,
)
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.users.models import Friendship, Profile
from api.users.permissions import CanAccessProfile
from api.users.serializers import (
    FriendshipSerializer,
    PasswordChangeSerializer,
    ProfileSerializer,
    PublicProfileSerializer,
    UpdateProfileSerializer,
)


class RegisterUserApiView(APIView):
    def post(self, request):
        serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():
            errors = Profile.check_unique(None, serializer.validated_data)
            if errors:
                return Response(
                    {"reason:": str(errors)}, status=status.HTTP_409_CONFLICT
                )

            password = serializer.validated_data["password"]
            password_hash = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            serializer.validated_data["password"] = password_hash

            user = serializer.save()

            profile = {
                "profile": {
                    "login": user.login,
                    "email": user.email,
                    "countryCode": user.countryCode,
                    "isPublic": user.isPublic,
                }
            }
            if user.phone is not None:
                profile["profile"]["phone"] = user.phone
            if user.image is not None:
                profile["profile"]["image"] = user.image

            return Response(profile, status=status.HTTP_201_CREATED)

        raise ValidationError(serializer.errors)


class SigninUserApiView(APIView):
    def post(self, request):
        login = request.data.get("login")
        password = request.data.get("password")
        user = Profile.objects.filter(login=login).first()

        if user is not None:
            if not bcrypt.checkpw(
                password.encode("utf-8"), user.password.encode("utf-8")
            ):
                raise NotAuthenticated(
                    {"error": "Invalid credentials"},
                )
        else:
            raise NotAuthenticated(
                {"error": "Invalid credentials"},
            )

        token = jwt.encode(
            {
                "id": user.id,
                "password": password,
                "exp": timezone.now() + timedelta(hours=24),
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return Response({"token": token})


class ProfileMeApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile_data = self._get_profile_data(user)
        return Response(profile_data)

    def patch(self, request):
        user = request.user
        serializer = UpdateProfileSerializer(
            user, data=request.data, partial=True
        )
        if serializer.is_valid():
            errors = Profile.check_unique(user.id, serializer.validated_data)
            if errors:
                return Response(
                    {"reason:": str(errors)}, status=status.HTTP_409_CONFLICT
                )
            serializer.save()

            return Response(self._get_profile_data(user))

        raise ValidationError(serializer.errors)

    def _get_profile_data(self, user):
        profile = {
            "login": user.login,
            "email": user.email,
            "countryCode": user.countryCode,
            "isPublic": user.isPublic,
        }

        if user.phone is not None:
            profile["phone"] = user.phone
        if user.image is not None:
            profile["image"] = user.image

        return profile


class ProfilesApiView(APIView):
    permission_classes = [IsAuthenticated, CanAccessProfile]

    def get(self, request, login):
        try:
            profile = Profile.objects.get(login=login)
            self.check_object_permissions(request, profile)
            serializer = PublicProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            raise PermissionDenied(
                {"detail": "Profile not found."},
            ) from None


class AddFriendApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            login = request.data.get("login")
            profile = Profile.objects.get(login=login)
            request.user.add_friend(profile)
            return Response(
                {"status": "ok"},
                status=status.HTTP_200_OK,
            )
        except Profile.DoesNotExist:
            raise NotFound(
                {"detail": "Profile not found."},
            ) from None


class RemoveFriendApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            login = request.data.get("login")
            profile = Profile.objects.get(login=login)
            request.user.remove_friend(profile)
            return Response(
                {"status": "ok"},
                status=status.HTTP_200_OK,
            )
        except Profile.DoesNotExist:
            raise NotFound(
                {"detail": "Profile not found."},
            ) from None


class FriendsListApiView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        class QueryParamsSerializer(serializers.Serializer):
            limit = serializers.IntegerField(default=5)
            offset = serializers.IntegerField(default=0)

        serializer = QueryParamsSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)

        limit = serializer.validated_data.get("limit")
        offset = serializer.validated_data.get("offset")

        return Friendship.objects.order_by("-addedAt").filter(
            from_profile=self.request.user
        )[offset: offset + limit]


class PasswordChangeApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data.get("oldPassword")
            new_password = serializer.validated_data.get("newPassword")

            if bcrypt.checkpw(
                old_password.encode("utf-8"),
                request.user.password.encode("utf-8"),
            ):
                password_hash = bcrypt.hashpw(
                    new_password.encode("utf-8"), bcrypt.gensalt()
                ).decode("utf-8")
                request.user.password = password_hash
                request.user.save()

                return Response({"status": "ok"}, status=status.HTTP_200_OK)

            raise PermissionDenied({"error": "Invalid old password"})

        raise ValidationError(serializer.errors)
