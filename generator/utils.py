import qrcode
from io import BytesIO
from django.core.files import File

def generate_qr_code(data):
    qr_img = qrcode.make(data)
    buffer = BytesIO()
    qr_img.save(buffer)
    return File(buffer, name='qr_code.png')
