from django.contrib import admin

from network.models import NetworkNode


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ("name", "type")
