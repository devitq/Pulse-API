import re

import bcrypt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import Profile
from users.serializers import UserSerializer

MIN_PASSWORD_LEN = 6
MAX_PASSWORD_LEN = 100


@api_view(["POST"])
def register_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        if (
            Profile.objects.filter(
                login=serializer.validated_data["login"]
            ).first()
            is not None
        ):
            return Response(
                {"error": "User with this login already exists"},
                status=status.HTTP_409_CONFLICT,
            )
        if (
            Profile.objects.filter(
                email=serializer.validated_data["email"]
            ).first()
            is not None
        ):
            return Response(
                {"error": "User with this email already exists"},
                status=status.HTTP_409_CONFLICT,
            )
        if (
            Profile.objects.filter(
                phone=serializer.validated_data["phone"]
            ).first()
            is not None
        ):
            return Response(
                {"error": "User with this phone already exists"},
                status=status.HTTP_409_CONFLICT,
            )

        password = serializer.validated_data["password"]
        password_pattern = re.compile(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{6,100}$"
        )

        if not (
            bool(re.match(password_pattern, password))
        ):
            error = {"message": "Your password does not meet our requirements"}
            return Response(
                error,
                status=status.HTTP_400_BAD_REQUEST,
            )

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
