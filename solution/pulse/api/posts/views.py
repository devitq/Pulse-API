from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.posts.models import Post
from api.posts.permissions import CanAccessPost
from api.posts.serializers import PostSerializer


class CreatePostApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ValidationError(serializer.errors)


class PostDetailApiView(APIView):
    permission_classes = [IsAuthenticated, CanAccessPost]

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            self.check_object_permissions(request, post)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            raise NotFound(
                {"detail": "Post not found."},
            ) from None
