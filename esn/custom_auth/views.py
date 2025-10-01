from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from custom_auth.serializers import AuthTokenSerializer


@extend_schema(
    tags=["Auth"],
    request=AuthTokenSerializer,
)
class CustomObtainAuthToken(ObtainAuthToken):
    pass


@extend_schema(tags=["Auth"])
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Token deleted"})
