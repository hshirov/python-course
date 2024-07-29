from django.urls import path
from .views import IndexView, create_post

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('post/create', create_post, name='create'),
]
