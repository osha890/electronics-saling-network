from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from products.models import Product
from products.serializers import ProductSerializer


@extend_schema(tags=["Products"])
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
