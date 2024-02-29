from django.urls import path

import users.views

urlpatterns = [
    path(
        "register",
        users.views.RegisterUserApiView.as_view(),
        name="register",
    ),
    path(
        "sign-in",
        users.views.SigninUserApiView.as_view(),
        name="sign-in",
    ),
    path(
        "protected-view",
        users.views.ProtectedView.as_view(),
    )
]
