from django.db.models import Q
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
            query = Q()
            for region in regions_list:
                query |= Q(region=region)
            queryset = queryset.filter(query)
        return queryset


class CountryByAlpha2View(RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = "alpha2"
