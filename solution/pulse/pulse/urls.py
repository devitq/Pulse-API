from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Built-in urls
    path("admin/", admin.site.urls),
    path(
        "api-auth/",
        include(
            "rest_framework.urls",
            namespace="rest_framework",
        ),
    ),
    # API
    path("api/ping/", include("ping.urls")),
    path("api/countries/", include("countries.urls")),
]

if settings.DEBUG:
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)
