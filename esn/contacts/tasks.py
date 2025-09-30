from celery import shared_task
from django.core.mail import EmailMessage
from django.utils import timezone

from contacts.utils import generate_qr_code, get_qr_data
from network.models import NetworkNode


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
