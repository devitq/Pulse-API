from django.urls import path

import api.posts.views

urlpatterns = [
    path(
        "/create",
        api.posts.views.CreatePostApiView.as_view(),
        name="create-post",
    ),
    path(
        "/<str:post_id>",
        api.posts.views.PostDetailApiView.as_view(),
        name="post-detail",
    ),
]
