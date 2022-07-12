import logging

from brew_notifier.celeryapp import app
from notifier.models import Event, Company
from celery import shared_task

default_logger = logging.getLogger("default")


@shared_task
def crawl_event(event_id, *args, **kwargs):
    event = Event.objects.get(id=event_id)
    default_logger.info(f"{event.link} crawled")


@shared_task
def connect_company_to_event(event_id, company_id):
    company = Company.objects.get(id=company_id)
    event = Event.objects.get(id=event_id)
    default_logger.info(
        f"connects company {company.name or company.name} to event {event.name or event.id}"
    )
