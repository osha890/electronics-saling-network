from rest_framework import serializers

from contacts.serializers import ContactSerializer
from network.models import NetworkNode
from products.models import Product
from products.serializers import ProductSerializer


class NetworkNodeOutputSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    products = ProductSerializer(many=True)

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


class NetworkNodeInputSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        many=True,
    )

    class Meta:
        model = NetworkNode
        fields = [
            "name",
            "type",
            "products",
            "supplier",
        ]
