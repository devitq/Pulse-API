from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100)
    alpha2 = models.CharField(max_length=2)
    alpha3 = models.CharField(max_length=3)
    region = models.CharField()

    def __str__(self):
        return self.name
