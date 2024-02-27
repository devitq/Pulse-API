from django.urls import path

import ping.views

urlpatterns = [
    path("", ping.views.PingView.as_view(), name="ping"),
]
