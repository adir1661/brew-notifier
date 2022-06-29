from abc import ABC
from notifier.consts import CRAWLING_STATUSES
import uuid
from django.db import models

ENTITY_TYPES = [
    "Event",
    "Company",
    "Webinar",
    "ContentItem",
    "CompanyForEvent",
    "CompanyForWebinar",
    "CompanyCompetitor",
]


class Entity(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    pass

    class Meta:
        abstract = True


class CrawlableModel(Entity):
    link = models.URLField(max_length=255)
    name = models.CharField(max_length=255)
    crawling_status = models.CharField(
        choices=[(v.value, v.name) for v in CRAWLING_STATUSES], max_length=255
    )
    is_deleted = models.BooleanField(default=False)
    is_blacklisted = models.BooleanField(default=False)
    last_crawled = models.DateTimeField(default=None, null=True)

    class Meta:
        abstract = True


class Event(CrawlableModel):
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    description = models.TextField()
    location = models.CharField(max_length=255)


class Webinar(CrawlableModel):
    start_date = models.DateTimeField()
    description = models.TextField()
    language = models.CharField(max_length=255)

    class META:
        unique_together = (
            "start_date",
            "link"
        )


class Company(CrawlableModel):
    employees_min = models.IntegerField()
    employees_max = models.IntegerField()


class ContentItem(CrawlableModel):
    link = models.CharField(max_length=255, unique=True)
    snippet = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class META:
        unique_together = (
            "link"
        )


class CompanyForEvent(Entity):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    is_blacklisted = models.BooleanField(default=False)


class CompanyForWebinar(Entity):
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    is_blacklisted = models.BooleanField(default=False)


class CompanyCompetitor(Entity):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company"
    )
    competitor = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="competitor"
    )
    is_deleted = models.BooleanField(default=False)
