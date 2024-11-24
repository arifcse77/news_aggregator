import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_aggregator.settings')

app = Celery('news_aggregator')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Configure periodic tasks
app.conf.beat_schedule = {
    'fetch-news-feeds': {
        'task': 'core.tasks.fetch_and_process_feeds',
        'schedule': crontab(minute='*/30'),  # Run every 30 minutes
    },
}