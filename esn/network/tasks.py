import random
import time

from celery import shared_task
from django.db import transaction
from django.utils import timezone

from network.models import NetworkNode


@shared_task
def increase_debt_to_supplier():
    network_nodes = list(NetworkNode.objects.exclude(supplier=None))
    for node in network_nodes:
        node.debt_to_supplier += random.randint(5, 500)
    with transaction.atomic():
        NetworkNode.objects.bulk_update(network_nodes, ["debt_to_supplier"])
    return f"Updated {len(network_nodes)} network nodes at {timezone.now()}"


@shared_task
def decrease_debt_to_supplier():
    network_nodes = list(NetworkNode.objects.exclude(supplier=None))
    for node in network_nodes:
        node.debt_to_supplier -= random.randint(100, 10_000)
        if node.debt_to_supplier < 0:
            node.debt_to_supplier = 0
    with transaction.atomic():
        NetworkNode.objects.bulk_update(network_nodes, ["debt_to_supplier"])
    return f"Updated {len(network_nodes)} network nodes at {timezone.now()}"


@shared_task
def clear_debt(ids):
    queryset = NetworkNode.objects.filter(id__in=ids)
    updated = queryset.update(debt_to_supplier=0)
    return f"{updated} objects have debt cleared"
