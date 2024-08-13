from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from . import permissions as custom_permissions
from .models import Post, Comment, Hashtag, Reaction
from .serializers import PostSerializer, CommentSerializer, HashtagSerializer, ReactionSerializer
from .mixins import SaveAuthorMixin, ListDestroyViewset, ListCreateDestroyViewset
from .filters import PostFilter, PostSearchFilter
from .decorators import paginate


class PostViewSet(SaveAuthorMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [custom_permissions.IsAuthorOrAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PostFilter
    ordering_fields = ['created_at']

    @paginate(CommentSerializer)
    @action(detail=True, methods=['get'])
    def comments(self, request, *args, **kwargs):
        post = self.get_object()
        comments = post.comments.all()
        return comments
    
    @paginate(PostSerializer)
    @action(detail=False, methods=['get'], filterset_class=PostSearchFilter)
    def search(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return queryset


class CommentViewSet(SaveAuthorMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [custom_permissions.CommentsCustomPermissions]


class HashtagViewSet(ListDestroyViewset):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    permission_classes = [permissions.IsAdminUser]


class ReactionViewSet(SaveAuthorMixin, ListCreateDestroyViewset):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
    permission_classes = [custom_permissions.ReactionsCustomPermissions]
