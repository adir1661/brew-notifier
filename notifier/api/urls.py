from notifier.api.views import (
    EventViewSet,
    CompanyViewSet,
    WebinarViewSet,
    ContentItemViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"event", EventViewSet, basename="Event")
router.register(r"company", CompanyViewSet, basename="Company")
router.register(r"contentItem", ContentItemViewSet, basename="ContentItem")
router.register(r"webinar", WebinarViewSet, basename="Webinar")

urlpatterns = router.urls
