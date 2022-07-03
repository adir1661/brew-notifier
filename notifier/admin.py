from django.contrib import admin
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


class CompanyForWebinarAdmin(admin.ModelAdmin):
    pass


class CompanyForEventInline(admin.TabularInline):
    model = CompanyForEvent


class CompanyForWebinarInline(admin.TabularInline):
    model = CompanyForWebinar


class CompanyAdmin(admin.ModelAdmin):
    inlines = [CompanyForEventInline, CompanyForWebinarInline]
    readonly_fields = ("last_crawled", "crawling_status")


class EventAdmin(admin.ModelAdmin):
    inlines = [CompanyForEventInline]
    readonly_fields = ("last_crawled", "crawling_status")


class WebinarAdmin(admin.ModelAdmin):
    inlines = [CompanyForWebinarInline]
    readonly_fields = ("last_crawled", "crawling_status")


class CompanyCompetitorAdmin(admin.ModelAdmin):
    pass


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
