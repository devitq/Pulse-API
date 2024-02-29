from django.urls import path

import users.views

urlpatterns = [
    path(
        "auth/register",
        users.views.RegisterUserApiView.as_view(),
        name="register",
    ),
    path(
        "auth/sign-in",
        users.views.SigninUserApiView.as_view(),
        name="sign-in",
    ),
    path(
        "me/profile",
        users.views.ProfileMeApiView.as_view(),
    )
]
