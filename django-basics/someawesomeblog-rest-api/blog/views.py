from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrAdminOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
