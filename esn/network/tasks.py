import random

from celery import shared_task
from django.core.mail import EmailMessage
from django.db import transaction
from django.utils import timezone

from network.models import NetworkNode
from network.utils import generate_qr_code, get_qr_data


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
def clear_debt(ids: list):
    queryset = NetworkNode.objects.filter(id__in=ids)
    updated = queryset.update(debt_to_supplier=0)
    return f"{updated} objects have debt cleared"


@shared_task
def send_qr_email(email: str, node_id: int):
    try:
        node = NetworkNode.objects.get(id=node_id)
    except NetworkNode.DoesNotExist:
        return f"Node with ID {node_id} does not exist. Email is not sent."

    data = get_qr_data(node)
    qr_bytes = generate_qr_code(data)
    email_msg = EmailMessage(
        subject=f"QR code for {node.name}",
        to=[email],
    )
    email_msg.attach(f"{node.name}_qr.png", qr_bytes.getvalue())
    email_msg.send()
    return f"Email is sent to {email} at {timezone.now()}"
