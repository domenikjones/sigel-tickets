from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from core.models import CoreSettings


class CoreAdmin(admin.ModelAdmin):
    pass


@admin.register(CoreSettings)
class CoreSettingsAdmin(CoreAdmin):
    def has_add_permission(self, request):
        # prevent adding more than one instance
        return not CoreSettings.objects.exists()

    def changelist_view(self, request, extra_context=None):
        # redirect to changelist if an instance already exists
        obj = CoreSettings.objects.first()
        if obj:
            return redirect(reverse("admin:core_coresettings_change", args=[obj.pk]))
        return super().changelist_view(request, extra_context=extra_context)
