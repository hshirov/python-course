from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from . import permissions as custom_permissions
from .models import Post, Comment, Hashtag, Reaction
from .serializers import PostSerializer, CommentSerializer, HashtagSerializer, ReactionSerializer
from .mixins import SaveAuthorMixin
from .filters import PostFilter, PostSearchFilter


class PostViewSet(SaveAuthorMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [custom_permissions.IsAuthorOrAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PostFilter
    ordering_fields = ['created_at']

    @action(detail=True, methods=['get'])
    def comments(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = CommentSerializer(post.comments.all(), many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], filterset_class=PostSearchFilter)
    def search(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
    
        serializer = self.get_serializer(queryset, many=True)
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
