from rest_framework import viewsets

from network.models import NetworkNode
from network.serializers import NetworkNodeOutputSerializer


class NetworkNodeReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        NetworkNode.objects.select_related("contact", "contact__address", "supplier")
        .prefetch_related("products")
        .all()
    )
    serializer_class = NetworkNodeOutputSerializer
