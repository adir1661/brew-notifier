from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
import requests
from notifier.consts import ErrorMessages

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
        link = self.cleaned_data['link']
        try:
            resp = requests.get(link)
        except requests.exceptions.RequestException as e:
            raise ValidationError(ErrorMessages.COMPANY_URL_NOT_VALID)

        if not resp.ok:
            raise ValidationError("Company link not valid.!")

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
    search_fields = ('name', 'link')

    inlines = [CompanyForEventInline, CompanyForWebinarInline]
    readonly_fields = ("last_crawled", "crawling_status")


class EventAdmin(admin.ModelAdmin):
    inlines = [CompanyForEventInline]
    readonly_fields = ("last_crawled", "crawling_status")


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
