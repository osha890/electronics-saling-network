from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from contacts.serializers import ContactQrRequestSerializer
from contacts.tasks import send_qr_email
from network.models import NetworkNode


@extend_schema(
    tags=["Contacts"],
    request=ContactQrRequestSerializer,
)
class ContactQrView(APIView):
    def post(self, request):
        serializer = ContactQrRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        node_id = serializer.validated_data["node_id"]
        email = request.user.email

        if not email:
            return Response(
                {"error": "Your email address is not specified"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not NetworkNode.objects.filter(id=node_id).exists():
            return Response(
                {"error": "NetworkNode not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        send_qr_email.delay(email, node_id)

        return Response(
            {f"Email with QR is sent to {email}"},
            status=status.HTTP_200_OK,
        )
