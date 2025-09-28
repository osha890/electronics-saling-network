from django.contrib import admin

from contacts.models import Address, Contact


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("email", "address")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("address")
