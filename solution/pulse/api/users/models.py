from django.core.validators import (
    MaxLengthValidator,
    RegexValidator,
)
from django.db import models

from api.users.validators import CountryCodeValidator


class Profile(models.Model):
    login = models.CharField(
        max_length=30,
        validators=[RegexValidator(r"^[a-zA-Z0-9-]+$")],
    )
    email = models.EmailField(max_length=50)
    password = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{6,100}$"),
        ],
    )
    # ruff: noqa: DJ001 N815
    countryCode = models.CharField(
        max_length=2,
        validators=[RegexValidator(r"[a-zA-Z]{2}"), CountryCodeValidator()],
    )
    isPublic = models.BooleanField()
    phone = models.CharField(
        max_length=20,
        validators=[MaxLengthValidator(20), RegexValidator(r"^\+\d+")],
        null=True,
    )
    image = models.URLField(max_length=200, null=True)
    friends = models.ManyToManyField(
        "self", through="Friendship", blank=True, symmetrical=False
    )

    def __str__(self):
        return self.login

    def is_authenticated(self):
        return True

    def add_friend(self, user):
        if self != user:
            self.friends.add(user)

    def remove_friend(self, user):
        self.friends.remove(user)

    def check_for_friendship(self, user):
        return self.friends.filter(pk=user.pk).exists()

    def like_post(self, post):
        self.disliked_posts.remove(post)
        return self.liked_posts.add(post)

    def dislike_post(self, post):
        self.liked_posts.remove(post)
        return self.disliked_posts.add(post)

    @classmethod
    def check_unique(cls, user_id, validated_data):
        errors = {}

        if (
            cls.objects.filter(login=validated_data.get("login"))
            .exclude(id=user_id)
            .exists()
        ):
            errors["login"] = {"User with this login already exists"}

        if (
            cls.objects.filter(email=validated_data.get("email"))
            .exclude(id=user_id)
            .exists()
        ):
            errors["email"] = {"User with this email already exists"}

        if (
            cls.objects.filter(phone=validated_data.get("phone"))
            .exclude(id=user_id)
            .exists()
        ) and validated_data.get("phone") is not None:
            errors["phone"] = {"User with this phone already exists"}

        return errors


class Friendship(models.Model):
    from_profile = models.ForeignKey(
        Profile, related_name="friendship_from", on_delete=models.CASCADE
    )
    to_profile = models.ForeignKey(
        Profile, related_name="friendship_to", on_delete=models.CASCADE
    )
    addedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_profile} -> {self.to_profile}"
