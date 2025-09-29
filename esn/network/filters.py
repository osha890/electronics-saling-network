import django_filters

from network.models import NetworkNode
from products.models import Product


class NetworkNodeFilter(django_filters.FilterSet):
    country = django_filters.CharFilter(
        field_name="contact__address__country",
        lookup_expr="iexact",
    )
    product = django_filters.ModelChoiceFilter(
        field_name="products",
        queryset=Product.objects.all(),
    )

    class Meta:
        model = NetworkNode
        fields = ["country", "product"]
