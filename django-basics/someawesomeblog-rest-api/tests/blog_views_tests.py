import pytest
from django.contrib.auth.models import User
from rest_framework import status
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
    
    def test_unauthenticated_user_cannot_create_post(self, api_client):
        data = {'title': 'Test Post', 'content': 'Test Content'}
        response = api_client.post('/posts/', data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_authenticated_user_can_create_post(self, api_client):
        user = User.objects.create_user(username='testuser', password='password')
        api_client.force_authenticate(user=user)

        data = {'title': 'Test Post', 'text_content': 'Test Content'}
        response = api_client.post('/posts/', data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Post.objects.count() == 1
