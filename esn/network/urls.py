from rest_framework.routers import DefaultRouter

from network.views import NetworkNodeReadOnlyViewSet

router = DefaultRouter()
router.register(r"network_nodes", NetworkNodeReadOnlyViewSet, basename="network_node")

urlpatterns = router.urls
