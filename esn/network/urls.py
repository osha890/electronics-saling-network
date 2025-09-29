from django.urls import path
from rest_framework.routers import DefaultRouter

from network.views import NetworkNodeHighDebtView, NetworkNodeViewSet

router = DefaultRouter()
router.register(r"network_nodes", NetworkNodeViewSet, basename="network_node")

urlpatterns = [
    path(
        "network_nodes/high-debt/", NetworkNodeHighDebtView.as_view(), name="high-debt"
    ),
] + router.urls
