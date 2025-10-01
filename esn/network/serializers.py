from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from contacts.serializers import ContactSerializer
from network.models import NetworkNode
from products.models import Product
from products.serializers import ProductSerializer


class NetworkNodeOutputSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = NetworkNode
        fields = [
            "id",
            "name",
            "type",
            "email",
            "country",
            "city",
            "street",
            "house_number",
            "products",
            "supplier",
            "debt_to_supplier",
            "created_at",
        ]


class NetworkNodeInputSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        many=True,
        required=False,
    )
    supplier = serializers.PrimaryKeyRelatedField(
        queryset=NetworkNode.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = NetworkNode
        fields = [
            "name",
            "type",
            "email",
            "country",
            "city",
            "street",
            "house_number",
            "products",
            "supplier",
        ]

    def validate_name(self, value):
        if len(value) > 50:
            raise serializers.ValidationError(
                "The name cannot be longer than 50 characters."
            )
        return value

    def validate(self, attrs):
        if self.instance:
            instance = NetworkNode(
                id=self.instance.id,
                name=attrs.get("name", self.instance.name),
                type=attrs.get("type", self.instance.type),
                supplier=attrs.get("supplier", self.instance.supplier),
            )
        else:
            instance = NetworkNode(**attrs)

        try:
            instance.clean()
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.error_list)

        return attrs
