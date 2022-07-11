from rest_framework.serializers import (
    ModelSerializer,
    SlugRelatedField,
    StringRelatedField,
)
from notifier.models import (
    Company,
    Webinar,
    ContentItem,
    Event,
    CompanyForEvent,
    CompanyCompetitor,
    CompanyForWebinar,
)
from notifier.utils import validate_company_url
from rest_framework.exceptions import ValidationError


class ContentItemSerializer(ModelSerializer):
    class Meta:
        model = ContentItem
        exclude = []


class CompanyForEventSerializer(ModelSerializer):
    class Meta:
        model = CompanyForEvent
        exclude = []


class CompanyForWebinarSerializer(ModelSerializer):
    class Meta:
        model = CompanyForWebinar
        exclude = []


class CompanySerializer(ModelSerializer):
    company_events = CompanyForEventSerializer(many=True, read_only=True)
    company_webinars = CompanyForWebinarSerializer(
        many=True,
        read_only=True,
    )
    company_content_items = ContentItemSerializer(many=True, read_only=False)

    def validate_link(self, value):
        validate_company_url(value, error_class=ValidationError)
        return value

    class Meta:
        model = Company
        exclude = []


class WebinarSerializer(ModelSerializer):
    webinar_companies = CompanyForWebinarSerializer(many=True, read_only=True)

    class Meta:
        model = Webinar
        exclude = []


class EventSerializer(ModelSerializer):
    event_companies = CompanyForEventSerializer(read_only=True, many=True)

    class Meta:
        model = Event
        exclude = []
