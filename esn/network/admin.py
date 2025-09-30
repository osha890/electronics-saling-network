from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html

from network.models import NetworkNode
from network.tasks import clear_debt as clear_debt_task


@admin.action(description="Clear dept")
def clear_debt(modeladmin, request, queryset):
    count = queryset.count()
    if count > 20:
        ids = list(queryset.values_list("id", flat=True))
        clear_debt_task.delay(ids)
        modeladmin.message_user(
            request,
            f"Debt clearing task for {count} objects has been scheduled asynchronously.",
            messages.WARNING,
        )
    else:
        updated = queryset.update(debt_to_supplier=0)
        modeladmin.message_user(
            request,
            f"{updated} objects have debt cleared",
            messages.SUCCESS,
        )


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
    actions = [clear_debt]

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
