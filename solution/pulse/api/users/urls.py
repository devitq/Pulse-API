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
        name="profile-me",
    ),
    path(
        "profiles/<str:login>",
        api.users.views.ProfileAPIView.as_view(),
        name="profiles",
    ),
    path(
        "friends/add",
        api.users.views.AddFriendAPIView.as_view(),
        name="add-friend",
    ),
    path(
        "friends/remove",
        api.users.views.RemoveFriendAPIView.as_view(),
        name="remove-friend",
    ),
]
