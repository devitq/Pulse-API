import uuid

from rest_framework import serializers, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.posts.models import Post
from api.posts.permissions import CanAccessFeed, CanAccessPost
from api.posts.serializers import PostSerializer
from api.users.models import Profile


class CreatePostApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise ValidationError(serializer.errors)


class PostDetailApiView(APIView):
    permission_classes = [IsAuthenticated, CanAccessPost]

    def get(self, request, post_id):
        try:
            uuid.UUID(post_id)
        except ValueError:
            raise NotFound from None

        try:
            post = Post.objects.get(id=post_id)
            self.check_object_permissions(request, post)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            raise NotFound(
                {"detail": "Post not found."},
            ) from None


class MyFeedListApiView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        class QueryParamsSerializer(serializers.Serializer):
            limit = serializers.IntegerField(default=5)
            offset = serializers.IntegerField(default=0)

        serializer = QueryParamsSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)

        limit = serializer.validated_data.get("limit")
        offset = serializer.validated_data.get("offset")

        return self.request.user.posts.order_by("-createdAt").all()[
            offset: offset + limit
        ]


class UserFeedListApiView(ListAPIView):
    permission_classes = [IsAuthenticated, CanAccessFeed]
    serializer_class = PostSerializer

    def get_queryset(self):
        class QueryParamsSerializer(serializers.Serializer):
            limit = serializers.IntegerField(default=5)
            offset = serializers.IntegerField(default=0)

        login = self.kwargs.get("login")

        try:
            user = Profile.objects.get(login=login)
        except Profile.DoesNotExist:
            raise NotFound(
                {"detail": "Profile not found."},
            ) from None

        self.check_object_permissions(self.request, user)

        serializer = QueryParamsSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)

        limit = serializer.validated_data.get("limit")
        offset = serializer.validated_data.get("offset")

        return user.posts.order_by("-createdAt").all()[offset: offset + limit]


class LikePostApiView(APIView):
    permission_classes = [IsAuthenticated, CanAccessPost]

    def post(self, request, post_id):
        try:
            uuid.UUID(post_id)
        except ValueError:
            raise NotFound from None

        try:
            post = Post.objects.get(id=post_id)
            self.check_object_permissions(request, post)
            request.user.like_post(post)
            serializer = PostSerializer(post)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except Post.DoesNotExist:
            raise NotFound(
                {"detail": "Post not found."},
            ) from None


class DislikePostApiView(APIView):
    permission_classes = [IsAuthenticated, CanAccessPost]

    def post(self, request, post_id):
        try:
            uuid.UUID(post_id)
        except ValueError:
            raise NotFound from None

        try:
            post = Post.objects.get(id=post_id)
            self.check_object_permissions(request, post)
            request.user.dislike_post(post)
            serializer = PostSerializer(post)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except Post.DoesNotExist:
            raise NotFound(
                {"detail": "Post not found."},
            ) from None
