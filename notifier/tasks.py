import logging

from notifier.models import Event
from celery import shared_task

default_logger = logging.getLogger("default")


@shared_task
def crawl_event(event_id, *args, **kwargs):
    event = Event.objects.get(id=event_id)
    default_logger.info(f"{event.link} crawled")
