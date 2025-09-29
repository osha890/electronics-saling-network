from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from network.models import NetworkNode


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "type",
        "supplier_link",
        "debt_to_supplier",
        "get_city",
    )
    raw_id_fields = ("supplier",)
    list_filter = ("contact__address__city",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("supplier", "contact__address")
        return qs

    @admin.display(description="Supplier", ordering="supplier__name")
    def supplier_link(self, obj):
        if obj.supplier_id:
            url = reverse("admin:network_networknode_change", args=[obj.supplier_id])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "—"

    def get_city(self, obj):
        try:
            return obj.contact.address.city
        except AttributeError:
            return "—"

    get_city.short_description = "City"
