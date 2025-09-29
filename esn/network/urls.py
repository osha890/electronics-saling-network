from django.urls import path
from rest_framework.routers import DefaultRouter

from network.views import NetworkNodeHighDebtView, NetworkNodeViewSet

router = DefaultRouter()
router.register(r"", NetworkNodeViewSet, basename="network_node")

urlpatterns = [
    path("high-debt/", NetworkNodeHighDebtView.as_view(), name="high-debt"),
] + router.urls
