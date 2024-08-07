import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'someawesomeblog.settings')

app = Celery('someawesomeblog')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete-old-posts-every-day': {
        'task': 'blog.tasks.delete_old_posts',
        'schedule': crontab(hour=0, minute=0)
    },
}
