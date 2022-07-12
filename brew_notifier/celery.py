import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brew_notifier.settings')

app = Celery('brew_notifier')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()