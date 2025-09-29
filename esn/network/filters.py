import django_filters

from network.models import NetworkNode


class NetworkNodeFilter(django_filters.FilterSet):
    country = django_filters.CharFilter(
        field_name="contact__address__country",
        lookup_expr="iexact",
    )

    class Meta:
        model = NetworkNode
        fields = ["country"]
