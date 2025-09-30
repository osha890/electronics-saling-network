from io import BytesIO

from qrcode.main import QRCode

from network.models import NetworkNode


def get_qr_data(node: NetworkNode) -> str:
    contact = node.contact
    address = contact.address if contact else None

    data = {
        "name": node.name,
        "email": contact.email if contact else "",
        "country": address.country if address else "",
        "city": address.city if address else "",
        "street": address.street if address else "",
        "house_number": address.house_number if address else "",
    }

    return "\n".join(f"{key}: {value}" for key, value in data.items())


def generate_qr_code(data: str) -> BytesIO:
    qr = QRCode()
    qr.add_data(data)
    img = qr.make_image()

    buffer = BytesIO()
    img.save(buffer)
    return buffer
