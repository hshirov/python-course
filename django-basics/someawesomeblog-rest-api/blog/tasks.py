from django.utils import timezone
from celery import shared_task
from django.db.models import Count
from .models import Post

@shared_task
def delete_old_posts():
    one_year_ago = timezone.now() - timezone.timedelta(days=365)
    old_posts = Post.objects.annotate(comment_count=Count('comments')).filter(
        created_at__lt=one_year_ago, comment_count=0)
    
    count, _ = old_posts.delete()

    return f'Deleted {count} old posts.'
