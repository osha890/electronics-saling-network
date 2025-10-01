from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from employees.models import Employee
from network.filters import NetworkNodeFilter
from network.models import NetworkNode
from network.serializers import NetworkNodeInputSerializer, NetworkNodeOutputSerializer
from network.tasks import send_qr_email


@extend_schema(tags=["Network Nodes"])
class NetworkNodeViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = NetworkNodeFilter

    def get_queryset(self):
        user = self.request.user

        qs = (
            NetworkNode.objects.select_related("supplier")
            .prefetch_related("products")
            .all()
        )

        if user.is_superuser:
            return qs

        try:
            employee = user.employee
        except Employee.DoesNotExist:
            return qs.none()

        return qs.filter(pk=employee.network_node_id)

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


@extend_schema(tags=["Network Nodes"])
class NetworkNodeHighDebtView(generics.ListAPIView):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeOutputSerializer

    def get_queryset(self):
        user = self.request.user

        qs = NetworkNode.objects.all()

        if user.is_superuser:
            return qs

        try:
            employee = user.employee
        except Employee.DoesNotExist:
            return qs.none()

        return qs.filter(pk=employee.network_node_id)

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


@extend_schema(tags=["Network Nodes"])
class ContactQrView(APIView):
    def post(self, request, id):
        email = request.user.email

        if not email:
            return Response(
                {"error": "Your email address is not specified"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not NetworkNode.objects.filter(id=id).exists():
            return Response(
                {"error": "NetworkNode not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        send_qr_email.delay(email, id)

        return Response(
            {f"Email with QR is sent to {email}"},
            status=status.HTTP_200_OK,
        )
