from abc import ABC
from notifier.consts import CRAWLING_STATUSES
from uuid import uuid4
from django.db import models


class Entity:
    pass


class CrawlableModel(models.Model, Entity):
    link = models.URLField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    crawling_status = models.CharField(
        choices=[(v.value, v.name) for v in CRAWLING_STATUSES],
        max_length=255,
        default=CRAWLING_STATUSES.NOT_CRAWLED,
    )
    is_deleted = models.BooleanField(default=False)
    is_blacklisted = models.BooleanField(default=False)
    last_crawled = models.DateTimeField(default=None, null=True)

    class Meta:
        abstract = True


class Event(CrawlableModel):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)


class Webinar(CrawlableModel):
    link = models.URLField(max_length=255)
    start_date = models.DateTimeField()
    description = models.TextField(blank=True)
    language = models.CharField(max_length=255, default="en")

    class META:
        unique_together = ("start_date", "link")


class Company(CrawlableModel):
    employees_min = models.PositiveIntegerField(blank=True, default=1)
    employees_max = models.PositiveIntegerField(blank=True, default=1)



class ContentItem(CrawlableModel):
    link = models.CharField(max_length=255, unique=True)
    snippet = models.CharField(max_length=255, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True)

    class META:
        unique_together = "link"


class CompanyForEvent(models.Model, Entity):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False, blank=True)
    is_blacklisted = models.BooleanField(default=False, blank=True)


class CompanyForWebinar(models.Model, Entity):
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    is_blacklisted = models.BooleanField(default=False)


class CompanyCompetitor(models.Model, Entity):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company"
    )
    competitor = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="competitor"
    )
    is_deleted = models.BooleanField(default=False)
