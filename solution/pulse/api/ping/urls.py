from django.urls import path

import api.ping.views

urlpatterns = [
    path("", api.ping.views.PingView.as_view(), name="ping"),
]
