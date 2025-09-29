from rest_framework import serializers

from contacts.models import Address, Contact


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "country",
            "city",
            "street",
            "house_number",
        ]


class ContactSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Contact
        fields = [
            "email",
            "address",
        ]
