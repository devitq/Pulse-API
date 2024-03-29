from django.urls import include, path

urlpatterns = [
    path("ping", include("api.ping.urls")),
    path("countries", include("api.countries.urls")),
    path("posts", include("api.posts.urls")),
    path("", include("api.users.urls")),
]
