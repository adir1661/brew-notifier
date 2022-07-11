from rest_framework.serializers import (
    ModelSerializer,
)
from notifier.models import (
    Event,
    Company,
    Webinar,
    ContentItem,
    CompanyForEvent,
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
    company_events = CompanyForEventSerializer(
        many=True,
        read_only=True,
        # required=True,
    )
    company_webinars = CompanyForWebinarSerializer(
        required=False,
        many=True,
        # read_only=True,
    )
    company_content_items = ContentItemSerializer(
        many=True,
        read_only=False,
        required=False,
    )

    def validate_link(self, value):
        validate_company_url(value, error_class=ValidationError)
        return value

    def create(self,*args,**kwargs):
        return super(self.__class__,self).create(*args,**kwargs)

    class Meta:
        model = Company
        exclude = []


class WebinarSerializer(ModelSerializer):
    webinar_companies = CompanyForWebinarSerializer(
        many=True, read_only=True, required=False
    )

    class Meta:
        model = Webinar
        exclude = []


class EventSerializer(ModelSerializer):
    event_companies = CompanyForEventSerializer(read_only=True, many=True)

    class Meta:
        model = Event
        exclude = []
