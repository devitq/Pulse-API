from django.conf import settings
from rest_framework import serializers

from api.posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    # ruff: noqa: N815
    author = serializers.ReadOnlyField(source="author.username")
    likesCount = serializers.SerializerMethodField()
    dislikesCount = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "content",
            "author",
            "tags",
            "createdAt",
            "likesCount",
            "dislikesCount",
        ]
        read_only_fields = ["id", "createdAt", "likesCount", "dislikesCount"]

    # ruff: noqa: N802
    def get_likesCount(self, obj):
        return obj.likes.count()

    def get_dislikesCount(self, obj):
        return obj.dislikes.count()

    def validate_tags(self, value):
        for tag in value:
            if len(tag) > settings.MAX_TAG_LENGTH:
                error = "Each tag must be 20 characters or fewer."
                raise serializers.ValidationError(error)
        return value
