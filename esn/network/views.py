from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from network.filters import NetworkNodeFilter
from network.models import NetworkNode
from network.serializers import NetworkNodeOutputSerializer


class NetworkNodeReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        NetworkNode.objects.select_related("contact", "contact__address", "supplier")
        .prefetch_related("products")
        .all()
    )
    serializer_class = NetworkNodeOutputSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = NetworkNodeFilter
