from django.urls import path

import countries.views

urlpatterns = [
    path("", countries.views.CountryListView.as_view(), name="countries"),
    path(
        "<str:alpha2>/",
        countries.views.CountryByAlpha2View.as_view(),
        name="country_by_alpha2",
    ),
]
