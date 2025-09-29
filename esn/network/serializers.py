from rest_framework import serializers

from contacts.serializers import ContactOutputSerializer
from network.models import NetworkNode
from products.serializers import ProductOutputSerializer


class NetworkNodeOutputSerializer(serializers.ModelSerializer):
    contact = ContactOutputSerializer()
    products = ProductOutputSerializer(many=True)

    class Meta:
        model = NetworkNode
        fields = [
            "id",
            "name",
            "type",
            "contact",
            "products",
            "supplier",
            "debt_to_supplier",
            "created_at",
        ]
