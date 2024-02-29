from django.urls import path

import users.views

urlpatterns = [
    path(
        "register",
        users.views.register_user,
        name="register",
    ),
]
