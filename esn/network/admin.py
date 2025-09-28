from django.contrib import admin

from network.models import NetworkNode


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "supplier", "debt_to_supplier", "created_at")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("supplier")
        return qs
