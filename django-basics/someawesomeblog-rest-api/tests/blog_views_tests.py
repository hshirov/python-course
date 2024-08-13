import pytest
from django.contrib.auth.models import User
from blog.models import Post

@pytest.mark.django_db
class TestPostView:
    @pytest.fixture
    def create_post(self):
        def make_post(**kwargs):
            return Post.objects.create(**kwargs)
        return make_post
    
    def test_list_posts(self, client, create_post):
        user = User.objects.create_user(username='testuser', password='password')
        create_post(title='Test Post 1', text_content='Text', author=user)
        create_post(title='Test Post 2', text_content='Text', author=user)

        response = client.get('/posts/')
        count = response.data.get('count')
        results = response.data.get('results')

        assert response.status_code == 200
        assert count == 2
        assert results[0].get('title') == 'Test Post 2'
