from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, HashtagViewSet, ReactionViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'hashtags', HashtagViewSet, basename='hashtag')
router.register(r'reactions', ReactionViewSet, basename='reaction')

urlpatterns = router.urls
