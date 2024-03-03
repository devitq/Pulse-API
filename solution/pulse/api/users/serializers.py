from django.core.validators import RegexValidator
from rest_framework import serializers

from api.users.models import Friendship, Profile


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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data["image"] is None:
            del data["image"]
        if data["phone"] is None:
            del data["phone"]
        return data


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


class FriendshipSerializer(serializers.ModelSerializer):
    login = serializers.SerializerMethodField()

    class Meta:
        model = Friendship
        fields = ["login", "addedAt"]

    def get_login(self, obj):
        return obj.to_profile.login


class PasswordChangeSerializer(serializers.Serializer):
    # ruff: noqa: N815
    oldPassword = serializers.CharField(required=True)
    newPassword = serializers.CharField(
        required=True,
        validators=[
            RegexValidator(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{6,100}$"),
        ],
    )
