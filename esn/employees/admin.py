from django.contrib import admin

from employees.models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("user", "network_node")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("user", "network_node")
        return qs
