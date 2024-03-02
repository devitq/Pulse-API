from django.urls import path

import api.countries.views

urlpatterns = [
    path("", api.countries.views.CountryListView.as_view(), name="countries"),
    path(
        "/<str:alpha2>",
        api.countries.views.CountryByAlpha2View.as_view(),
        name="country_by_alpha2",
    ),
]
