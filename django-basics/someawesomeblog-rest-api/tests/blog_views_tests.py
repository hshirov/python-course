import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from blog.models import Post


@pytest.mark.django_db
class TestPostView:
    post_list_url = reverse('post-list')

    @pytest.fixture
    def create_post(self):
        def make_post(**kwargs):
            return Post.objects.create(**kwargs)
        return make_post
    
    def test_list_posts(self, client, create_post):
        user = User.objects.create_user(username='testuser', password='password')
        create_post(title='Test Post 1', text_content='Text', author=user)
        create_post(title='Test Post 2', text_content='Text', author=user)

        response = client.get(self.post_list_url)
        count = response.data.get('count')
        results = response.data.get('results')

        assert response.status_code == 200
        assert count == 2
        assert results[0].get('title') == 'Test Post 2'
    
    def test_unauthenticated_user_cannot_create_post(self, api_client):
        data = {'title': 'Test Post', 'content': 'Test Content'}
        response = api_client.post(self.post_list_url, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_authenticated_user_can_create_post(self, api_client):
        user = User.objects.create_user(username='testuser', password='password')
        api_client.force_authenticate(user=user)

        data = {'title': 'Test Post', 'text_content': 'Test Content'}
        response = api_client.post(self.post_list_url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Post.objects.count() == 1
    
    def test_user_can_update_own_post(self, api_client, create_post):
        user = User.objects.create_user(username='testuser', password='password')
        post = create_post(title='Test Post 1', text_content='Text', author=user)

        api_client.force_authenticate(user=user)
        url = reverse('post-detail', args=[post.id])
        data = {'title': 'New Title', 'text_content': 'New Content'}
        response = api_client.put(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert Post.objects.get(id=post.id).title == 'New Title'
        assert Post.objects.get(id=post.id).text_content == 'New Content'
    
    def test_user_can_delete_own_post(self, api_client, create_post):
        user = User.objects.create_user(username='testuser', password='password')
        post = create_post(title='Test Post 1', text_content='Text', author=user)

        api_client.force_authenticate(user=user)
        url = reverse('post-detail', args=[post.id])
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Post.objects.filter(id=post.id).exists()
    
    def test_user_cannot_update_not_own_post(self, api_client, create_post):
        author_user = User.objects.create_user(username='testuser', password='password')
        post = create_post(title='Old Title', text_content='Old Content', author=author_user)

        not_author_user = User.objects.create_user(username='testuser2', password='password')
        api_client.force_authenticate(user=not_author_user)

        url = reverse('post-detail', args=[post.id])
        data = {'title': 'New Title', 'text_content': 'New Content'}
        response = api_client.put(url, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Post.objects.get(id=post.id).title == 'Old Title'
        assert Post.objects.get(id=post.id).text_content == 'Old Content'
    
    def test_user_cannot_delete_not_own_post(self, api_client, create_post):
        author_user = User.objects.create_user(username='testuser', password='password')
        post = create_post(title='Test Post 1', text_content='Text', author=author_user)

        not_author_user = User.objects.create_user(username='testuser2', password='password')
        api_client.force_authenticate(user=not_author_user)

        url = reverse('post-detail', args=[post.id])
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Post.objects.filter(id=post.id).exists()
