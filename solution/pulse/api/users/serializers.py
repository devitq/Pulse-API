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


class PublicProfileSerializer(serializers.ModelSerializer):
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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data["image"] is None:
            del data["image"]
        if data["phone"] is None:
            del data["phone"]
        return data
