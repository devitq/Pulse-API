from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView

from countries.models import Country
from countries.serializers import CountrySerializer


class CountryListView(ListAPIView):
    queryset = Country.objects.all().order_by("alpha2")
    serializer_class = CountrySerializer

    def filter_queryset(self, queryset):
        regions = self.request.query_params.get("region")
        if regions:
            regions_list = regions.split(",")
            invalid_regions = [
                region
                for region in regions_list
                if region not in settings.REGIONS
            ]
            if invalid_regions:
                invalid_regions_str = ", ".join(invalid_regions)
                error_message = f"Invalid region(s): {invalid_regions_str}"
                raise ValidationError(error_message)

            queryset = queryset.filter(region__in=regions_list)
        return queryset


class CountryByAlpha2View(RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = "alpha2"
