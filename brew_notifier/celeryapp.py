import os
from celery import Celery
from django.conf import settings
from kombu import Queue

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brew_notifier.settings")

app = Celery("brew_notifier")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


if __name__ == "__main__":
    app.start()
