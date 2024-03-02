from rest_framework import serializers

from api.countries.models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["name", "alpha2", "alpha3", "region"]
