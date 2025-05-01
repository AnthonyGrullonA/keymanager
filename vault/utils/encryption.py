# vault/utils/encryption.py
from cryptography.fernet import Fernet
from django.conf import settings
import base64


def get_fernet():
    try:
        raw_key = settings.PASSWORD_ENCRYPTION_KEY
        print(f"[DEBUG] Clave cruda desde settings: {repr(raw_key)}")
        print(f"[DEBUG] Longitud del string base64: {len(raw_key)}")

        key_bytes = raw_key.encode()
        decoded = base64.urlsafe_b64decode(key_bytes)
        print(f"[DEBUG] Longitud de la clave decodificada: {len(decoded)}")  # Debe ser 32

        return Fernet(key_bytes)
    except Exception as e:
        raise ValueError(f"[ERROR] Clave Fernet inválida: {e}")
