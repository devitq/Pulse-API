from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView

from api.countries.models import Country
from api.countries.serializers import CountrySerializer


class CountryListApiView(ListAPIView):
    queryset = Country.objects.all().order_by("alpha2")
    serializer_class = CountrySerializer

    def filter_queryset(self, queryset):
        regions = self.request.query_params.getlist("region")

        if regions == [""]:
            return queryset

        if regions:
            invalid_regions = [
                region for region in regions if region not in settings.REGIONS
            ]
            if invalid_regions:
                invalid_regions_str = ", ".join(invalid_regions)
                error_message = f"Invalid region(s): {invalid_regions_str}"
                raise ValidationError(error_message)

            queryset = queryset.filter(region__in=regions)

        return queryset


class CountryByAlpha2ApiView(RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = "alpha2"
