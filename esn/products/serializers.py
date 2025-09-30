from django.utils import timezone
from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "model",
            "release_date",
        ]
        read_only_fields = [
            "id",
        ]

    def validate_name(self, value):
        if len(value) > 25:
            raise serializers.ValidationError(
                "The name cannot be longer than 25 characters."
            )
        return value

    def validate_release_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("The date cannot be later than today.")
        return value
