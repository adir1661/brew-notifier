from rest_framework.serializers import ModelSerializer
from notifier.models import Company, Webinar, ContentItem, Event


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        exclude = []


class WebinarSerializer(ModelSerializer):
    class Meta:
        model = Webinar
        exclude = []


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        exclude = []


class ContentItemSerializer(ModelSerializer):
    class Meta:
        model = ContentItem
        exclude = []
