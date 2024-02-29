from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)
from django.db import models


class Profile(models.Model):
    login = models.CharField(
        max_length=30,
        validators=[RegexValidator(r"[a-zA-Z0-9-]+")],
    )
    email = models.EmailField(max_length=50)
    password = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(6),
            MaxLengthValidator(100),
            RegexValidator(r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).+$"),
        ],
    )
    # ruff: noqa: DJ001 N815
    countryCode = models.CharField(
        max_length=2,
        validators=[RegexValidator(r"[a-zA-Z]{2}")],
    )
    isPublic = models.BooleanField()
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r"\+[\d]+")],
        blank=True,
        null=True,
    )
    image = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.login
