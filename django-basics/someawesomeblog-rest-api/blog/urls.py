from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, HashtagViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'hashtags', HashtagViewSet, basename='hashtag')

urlpatterns = [
    path('', include(router.urls))
]
