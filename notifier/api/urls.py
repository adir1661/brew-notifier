from notifier.api.views import EventViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'event', EventViewSet, basename='event')

urlpatterns = router.urls
