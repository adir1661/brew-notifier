from rest_framework.viewsets import ModelViewSet
from notifier.models import Event, Company, ContentItem, Webinar
from notifier.api.serializers import (
    EventSerializer,
    CompanySerializer,
    ContentItemSerializer,
    WebinarSerializer,
)


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class WebinarViewSet(ModelViewSet):
    queryset = Webinar.objects.all()
    serializer_class = WebinarSerializer


class ContentItemViewSet(ModelViewSet):
    queryset = ContentItem.objects.all()
    serializer_class = ContentItemSerializer
