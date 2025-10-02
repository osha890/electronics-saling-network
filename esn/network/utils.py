from io import BytesIO

from qrcode.main import QRCode

from network.models import NetworkNode


def get_qr_data(node: NetworkNode) -> str:
    data = {
        "name": node.name,
        "email": node.email or "—",
        "country": node.country or "—",
        "city": node.city or "—",
        "street": node.street or "—",
        "house_number": node.house_number or "—",
    }

    return "\n".join(f"{key}: {value}" for key, value in data.items())


def generate_qr_code(data: str) -> BytesIO:
    qr = QRCode()
    qr.add_data(data)
    img = qr.make_image()

    buffer = BytesIO()
    img.save(buffer)
    return buffer
