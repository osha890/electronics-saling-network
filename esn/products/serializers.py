from rest_framework import serializers

from products.models import Product


class ProductOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "model",
            "release_date",
        ]
