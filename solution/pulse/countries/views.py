from rest_framework.generics import ListAPIView, RetrieveAPIView

from countries.models import Country
from countries.serializers import CountrySerializer


class CountryListView(ListAPIView):
    queryset = Country.objects.all().order_by("alpha2")
    filterset_fields = ["region"]
    serializer_class = CountrySerializer


class CountryByAlpha2View(RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = "alpha2"
