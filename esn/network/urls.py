from django.urls import path
from rest_framework.routers import DefaultRouter

from network.views import ContactQrView, NetworkNodeHighDebtView, NetworkNodeViewSet

router = DefaultRouter()
router.register(r"", NetworkNodeViewSet, basename="network_node")

urlpatterns = [
    path("high-debt/", NetworkNodeHighDebtView.as_view(), name="high-debt"),
    path("<int:id>/send-contact-qr/", ContactQrView.as_view(), name="send-contact-qr"),
] + router.urls
