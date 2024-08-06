from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from . import permissions as custom_permissions
from .models import Post, Comment, Hashtag, Reaction
from .serializers import PostSerializer, CommentSerializer, HashtagSerializer, ReactionSerializer
from .mixins import SaveAuthorMixin


class PostViewSet(SaveAuthorMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [custom_permissions.IsAuthorOrAdminOrReadOnly]

    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def comments(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = CommentSerializer(post.comments.all(), many=True)
        return Response(serializer.data)


class CommentViewSet(SaveAuthorMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [custom_permissions.CommentsCustomPermissions]


class HashtagViewSet(mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    permission_classes = [permissions.IsAdminUser]


class ReactionViewSet(SaveAuthorMixin,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
    permission_classes = [custom_permissions.ReactionsCustomPermissions]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['author'] = self.request.user
        return context
