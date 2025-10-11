simport os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GBV.settings')
django.setup()

from aReport.models import Report

def test_encryption():
    """Test encryption and decryption functionality"""
    test_message = "This is a test message for encryption."

    print("Original message:", test_message)

    # Encrypt
    encrypted = Report.encrypt_field(test_message)
    print("Encrypted:", encrypted)

    # Decrypt
    decrypted = Report.decrypt_field(encrypted)
    print("Decrypted:", decrypted)

    # Check if decryption matches original
    if decrypted == test_message:
        print("✅ Encryption and decryption work correctly!")
    else:
        print("❌ Encryption/decryption failed!")

if __name__ == "__main__":
    test_encryption()
