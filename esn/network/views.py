from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from network.filters import NetworkNodeFilter
from network.models import NetworkNode
from network.serializers import NetworkNodeInputSerializer, NetworkNodeOutputSerializer


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = (
        NetworkNode.objects.select_related("contact", "contact__address", "supplier")
        .prefetch_related("products")
        .all()
    )

    filter_backends = [DjangoFilterBackend]
    filterset_class = NetworkNodeFilter

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return NetworkNodeInputSerializer
        return NetworkNodeOutputSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        output_serializer = NetworkNodeOutputSerializer(
            instance, context=self.get_serializer_context()
        )
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        output_serializer = NetworkNodeOutputSerializer(
            instance, context=self.get_serializer_context()
        )
        return Response(output_serializer.data)


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
