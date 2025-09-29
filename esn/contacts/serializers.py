from rest_framework import serializers

from contacts.models import Address, Contact


class AddressOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "country",
            "city",
            "street",
            "house_number",
        ]


class ContactOutputSerializer(serializers.ModelSerializer):
    address = AddressOutputSerializer()

    class Meta:
        model = Contact
        fields = [
            "email",
            "address",
        ]
