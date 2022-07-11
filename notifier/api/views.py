from copy import deepcopy

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
from notifier.notifier import notification_reducer


class DeleteMixin:
    def destroy(self, request, pk=None, **kwargs):
        entity = self.get_object()
        self.perform_destroy(entity)
        return Response(f"{entity.__str__()} field is_deleted is now true", status=200)


class NotifierMixin:
    def perform_destroy(self, instance):
        original_entity = deepcopy(instance)
        instance.is_deleted = True
        instance.save()
        notification_reducer(
            original_entity_obj=original_entity,
            entity_obj=instance,
            entity_type=instance.__class__.__name__,
            options={"log_message": True},
        )

    def perform_create(self, serializer):
        entity_type = self.serializer_class.Meta.model.__name__
        entity = serializer.save()

        notification_reducer(
            original_entity_obj=None,
            entity_obj=entity,
            entity_type=entity_type,
            options={"log_message": True},
        )

    def perform_update(self, serializer):
        original_entity = deepcopy(serializer.instance)
        entity_type = self.serializer_class.Meta.model.__name__
        entity = serializer.save()
        notification_reducer(
            original_entity_obj=original_entity,
            entity_obj=entity,
            entity_type=entity_type,
            options={"log_message": True},
        )


class IsAdminOrApiKey(IsAdminUser):
    def has_permission(self, request, view):
        # overrides the isAdminUser action.
        admin_permissions = super(IsAdminOrApiKey, self).has_permission(request, view)

        is_api_key = request.headers.get("x-api-key") == "123456789"
        return admin_permissions or is_api_key


class EventViewSet(
    NotifierMixin,
    DeleteMixin,
    ModelViewSet,
):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrApiKey]


class CompanyViewSet(
    NotifierMixin,
    DeleteMixin,
    ModelViewSet,
):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminOrApiKey]

    def perform_destroy(self, instance):
        instance_copy = deepcopy(instance)
        instance_copy.is_deleted = False

        notification_reducer(
            original_entity_obj=instance, entity_obj=instance_copy, entity_type="none"
        )


class WebinarViewSet(
    NotifierMixin,
    DeleteMixin,
    ModelViewSet,
):
    queryset = Webinar.objects.all()
    serializer_class = WebinarSerializer
    permission_classes = [IsAdminOrApiKey]


class ContentItemViewSet(
    NotifierMixin,
    DeleteMixin,
    ModelViewSet,
):
    queryset = ContentItem.objects.all()
    serializer_class = ContentItemSerializer
    permission_classes = [IsAdminOrApiKey]
