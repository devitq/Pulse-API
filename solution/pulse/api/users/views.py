from datetime import timedelta

import bcrypt
import jwt
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.users.models import Profile
from api.users.serializers import ProfileSerializer, UpdateProfileSerializer


class RegisterUserApiView(APIView):
    def post(self, request):
        serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():
            errors = Profile.check_unique(None, serializer.validated_data)
            if errors:
                return Response(errors, status=status.HTTP_409_CONFLICT)

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

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SigninUserApiView(APIView):
    def post(self, request):
        login = request.data.get("login")
        password = request.data.get("password")
        user = Profile.objects.filter(login=login).first()

        if user is not None:
            if not bcrypt.checkpw(
                password.encode("utf-8"), user.password.encode("utf-8")
            ):
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
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
                return Response(errors, status=status.HTTP_409_CONFLICT)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
