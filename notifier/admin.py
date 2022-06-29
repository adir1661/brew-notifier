from django.contrib import admin
from notifier import models as notifier_models

# Register your models here.


class EventAdmin(admin.ModelAdmin):
    pass


admin.site.register(notifier_models.Event, EventAdmin)
