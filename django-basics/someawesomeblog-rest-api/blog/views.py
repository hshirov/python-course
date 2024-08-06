from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment, Hashtag
from .serializers import PostSerializer, CommentSerializer, HashtagSerializer
from .permissions import IsAuthorOrAdminOrReadOnly, CommentsCustomPermissions, IsAdminOrReadOnly
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


class HashtagViewSet(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    permission_classes = [IsAdminOrReadOnly]
