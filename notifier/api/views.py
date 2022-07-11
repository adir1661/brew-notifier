from rest_framework.viewsets import ModelViewSet
from notifier.models import Event, Company, ContentItem, Webinar
from notifier.api.serializers import (
    EventSerializer,
    CompanySerializer,
    ContentItemSerializer,
    WebinarSerializer,
)
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


class DeleteMixin:
    def destroy(self, request, pk=None, **kwargs):
        entity = self.queryset.get(id=pk)
        entity.is_deleted = True
        entity.save()
        return Response(f'{entity.name}\'s field is_deleted is now true', status=200)


class IsAdminOrApiKey(IsAdminUser):
    def has_permission(self, request, view):
        # overrides the isAdminUser action.
        admin_permissions = super(IsAdminOrApiKey, self).has_permission(request, view)

        is_api_key = request.headers.get("x-api-key") == "123456789"
        return admin_permissions or is_api_key


class EventViewSet(
    DeleteMixin,
    ModelViewSet,
):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrApiKey]


class CompanyViewSet(DeleteMixin, ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminOrApiKey]


class WebinarViewSet(ModelViewSet, DeleteMixin):
    queryset = Webinar.objects.all()
    serializer_class = WebinarSerializer
    permission_classes = [IsAdminOrApiKey]


class ContentItemViewSet(ModelViewSet, DeleteMixin):
    queryset = ContentItem.objects.all()
    serializer_class = ContentItemSerializer
    permission_classes = [IsAdminOrApiKey]
