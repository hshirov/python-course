from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrAdminOrReadOnly, CommentsCustomPermissions
from .mixins import SaveAuthorMixin


class PostViewSet(SaveAuthorMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly]

    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def comments(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = CommentSerializer(post.comments.all(), many=True)
        return Response(serializer.data)


class CommentViewSet(SaveAuthorMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CommentsCustomPermissions]

