from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
import requests
from notifier.consts import ErrorMessages
from notifier.tasks import crawl_event as celery_crawl_event, connect_company_to_event

from notifier.utils import validate_company_url
from notifier.models import (
    Event,
    Webinar,
    ContentItem,
    Company,
    CompanyCompetitor,
    CompanyForEvent,
    CompanyForWebinar,
)


classes_to_register = [
    Event,
    Webinar,
    ContentItem,
    CompanyCompetitor,
    CompanyForEvent,
    CompanyForWebinar,
]


class CompanyForEventAdmin(admin.ModelAdmin):
    pass


class CompanyAddForm(forms.ModelForm):
    def clean_link(self):
        link = self.cleaned_data["link"]

        validate_company_url(link, error_class=ValidationError)

        return link

    class Meta:
        model = Company
        exclude = []


class CompanyForWebinarAdmin(admin.ModelAdmin):
    pass


class CompanyForEventInline(admin.TabularInline):
    model = CompanyForEvent




class CompanyForWebinarInline(admin.TabularInline):
    model = CompanyForWebinar


class CompanyAdmin(admin.ModelAdmin):
    form = CompanyAddForm
    search_fields = ("name", "link")

    inlines = [CompanyForEventInline, CompanyForWebinarInline]
    readonly_fields = ("last_crawled", "crawling_status")


class EventAdmin(admin.ModelAdmin):
    inlines = [CompanyForEventInline]
    readonly_fields = ("last_crawled", "crawling_status")

    actions = ["crawl_event"]

    @admin.action()
    def crawl_event(self, request, queryset):
        for item in queryset:
            celery_crawl_event.apply_async(
                kwargs={"event_id": item.id}, queue="regular"
            )

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            connect_company_to_event.apply_async(
                kwargs=dict(
                    event_id=instance.event.id, company_id=instance.company.id
                ),
            )
            instance.save()
        formset.save_m2m()

    def save_model(self, request, obj, form, change):
        obj.save()
        celery_crawl_event.apply(kwargs={"event_id": obj.id})


class WebinarAdmin(admin.ModelAdmin):
    inlines = [CompanyForWebinarInline]
    readonly_fields = ("last_crawled", "crawling_status")


class CompanyCompetitorAdmin(admin.ModelAdmin):
    autocomplete_fields = ["company", "competitor"]


class ContentItemAdmin(admin.ModelAdmin):
    pass

    readonly_fields = ("last_crawled", "crawling_status")


admin.site.register(ContentItem, ContentItemAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Webinar, WebinarAdmin)
admin.site.register(CompanyForEvent, CompanyForEventAdmin)
admin.site.register(CompanyForWebinar, CompanyForWebinarAdmin)
admin.site.register(CompanyCompetitor, CompanyCompetitorAdmin)
