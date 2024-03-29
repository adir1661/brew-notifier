from notifier.consts import CRAWLING_STATUSES
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

    def __str__(self):
        return f"{self.name} ({self.link})"

    class Meta:
        abstract = True


class Event(CrawlableModel):
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)




class Webinar(CrawlableModel):
    start_date = models.DateTimeField()
    description = models.TextField(blank=True)
    language = models.CharField(max_length=255, default="en")

    class Meta:
        unique_together = ("start_date", "link")


class Company(CrawlableModel):
    employees_min = models.PositiveIntegerField(blank=True, default=1)
    employees_max = models.PositiveIntegerField(blank=True, default=1)

    def __str__(self):
        return f"{self.name} ({self.link})"

    class Meta:
        verbose_name_plural = "Companies"


class ContentItem(CrawlableModel):
    link = models.URLField(unique=True)
    snippet = models.CharField(max_length=255, blank=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="company_content_items",
    )


class CompanyForEvent(models.Model, Entity):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="event_companies"
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_events"
    )
    is_deleted = models.BooleanField(default=False, blank=True)
    is_blacklisted = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f"{self.company.name} => {self.event.name}"


class CompanyForWebinar(models.Model, Entity):
    webinar = models.ForeignKey(
        Webinar, on_delete=models.CASCADE, related_name="webinar_companies"
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_webinars"
    )
    is_deleted = models.BooleanField(default=False)
    is_blacklisted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company.name} => {self.webinar.name}"


class CompanyCompetitor(models.Model, Entity):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="competitor_companies"
    )
    competitor = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="competitors"
    )
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company.name} vs. ({self.competitor.name})"
