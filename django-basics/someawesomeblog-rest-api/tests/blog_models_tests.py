import pytest
from django.utils import timezone
from django.db import IntegrityError
from django.contrib.auth.models import User
from blog.models import Post


@pytest.mark.django_db
class TestPostModel:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='password')
    
    @pytest.fixture
    def post(self, user):
        return Post.objects.create(
            title='Test Post',
            text_content='Test post text #testhashtag',
            author=user
        )
    
    def test_post_str(self, post):
        assert str(post) == 'Test Post'

    def test_post_creation(self, post):
        assert post.title == 'Test Post'
        assert post.text_content == 'Test post text #testhashtag'
        assert post.author.username == 'testuser'
        assert post.created_at <= timezone.now()
    
    def test_post_author(self, post, user):
        assert post.author == user
    
    def test_create_post_without_title(self, user):
        with pytest.raises(IntegrityError):
            Post.objects.create(
                title=None,
                text_content='This is a post without a title',
                author=user
            )
    
    def test_create_post_without_text_content(self, user):
        with pytest.raises(IntegrityError):
            Post.objects.create(
                title='Test Post',
                text_content=None,
                author=user
            )
    
    def test_hashtags_are_added(self, post):
        assert post.hashtags.count() == 1
        assert post.hashtags.filter(name='testhashtag').exists()
