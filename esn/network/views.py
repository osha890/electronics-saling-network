from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.response import Response

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


class NetworkNodeHighDebtView(generics.ListAPIView):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeOutputSerializer

    def list(self, request, *args, **kwargs):
        avg_debt = NetworkNode.objects.exclude(
            supplier=None,
        ).aggregate(
            avg=Avg("debt_to_supplier"),
        )["avg"]
        queryset = self.get_queryset().filter(debt_to_supplier__gt=avg_debt)
        serializer = self.get_serializer(queryset, many=True)
        data = {"average_debt": avg_debt, "nodes": serializer.data}
        return Response(data)
