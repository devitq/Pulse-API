from rest_framework import serializers

from api.users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "login",
            "email",
            "password",
            "countryCode",
            "isPublic",
            "phone",
            "image",
        ]


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "login",
            "email",
            "countryCode",
            "isPublic",
            "phone",
            "image",
        ]
