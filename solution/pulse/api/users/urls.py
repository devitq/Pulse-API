from django.urls import path

import api.users.views

urlpatterns = [
    path(
        "auth/register",
        api.users.views.RegisterUserApiView.as_view(),
        name="register",
    ),
    path(
        "auth/sign-in",
        api.users.views.SigninUserApiView.as_view(),
        name="sign-in",
    ),
    path(
        "me/profile",
        api.users.views.ProfileMeApiView.as_view(),
    )
]
