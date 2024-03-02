from django.urls import include, path

urlpatterns = [
    path("ping", include("api.ping.urls")),
    path("countries", include("api.countries.urls")),
    path("", include("api.users.urls")),
]
