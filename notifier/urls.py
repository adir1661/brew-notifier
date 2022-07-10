from django.urls import path, include
# from notifier.api.urls import urls as api_urls
from . import views

urlpatterns = [
    path("api/", include("notifier.api.urls")),
    path("", views.index, name="index"),
]
