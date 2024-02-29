from rest_framework import serializers

from users.models import Profile


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

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
