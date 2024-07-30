from django.urls import path
from .views import IndexView, HashtagPostsView, PostDetail, create_post

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('hashtag/<str:hashtag>', HashtagPostsView.as_view(), name='posts_by_hashtag'),
    path('post/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('post/create', create_post, name='create'),
]
