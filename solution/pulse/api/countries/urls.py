from django.urls import path

import api.countries.views

urlpatterns = [
    path(
        "", api.countries.views.CountryListApiView.as_view(), name="countries"
    ),
    path(
        "/<str:alpha2>",
        api.countries.views.CountryByAlpha2ApiView.as_view(),
        name="country_by_alpha2",
    ),
]
