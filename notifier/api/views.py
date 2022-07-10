from rest_framework.viewsets import ModelViewSet
from notifier.models import Event
from notifier.api.serializers import EventSerializer


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
