import uuid

from django.db import models

from api.users.models import Profile


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    content = models.TextField(max_length=1000)
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    tags = models.JSONField()
    # ruff: noqa: N815
    createdAt = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        Profile, related_name="liked_posts", blank=True
    )
    dislikes = models.ManyToManyField(
        Profile, related_name="disliked_posts", blank=True
    )

    def __str__(self):
        return self.content
