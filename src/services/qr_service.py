# src/services/qr_service.py
"""QR Code Service"""
import os
import qrcode
from src.utils.helpers import get_receipt_dir
from src.utils.logger import get_logger

logger = get_logger(__name__)


def generate_qr_code(data, receipt_no):
    """Generate QR code image and save to disk"""
    try:
        # Create QR directory
        qr_dir = os.path.join(get_receipt_dir(), "qr")
        os.makedirs(qr_dir, exist_ok=True)
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            box_size=6,
            border=2
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save with receipt number
        qr_filename = f"{receipt_no}_qr.png"
        qr_path = os.path.join(qr_dir, qr_filename)
        img.save(qr_path)
        
        logger.info(f"QR code generated: {qr_path}")
        return qr_path
        
    except Exception as e:
        logger.error(f"QR generation error: {e}")
        return None


def generate_qr_code_data(payment_data):
    """Generate QR code data string from payment info"""
    return f"Receipt:{payment_data.get('receipt_number')}|Student:{payment_data.get('student_name')}|Amount:{payment_data.get('amount')}|Date:{payment_data.get('payment_date')}"


def generate_qr_code_for_payment(payment):
    """Generate QR code for payment data"""
    data = generate_qr_code_data(payment)
    return generate_qr_code(data, payment.get('receipt_number'))