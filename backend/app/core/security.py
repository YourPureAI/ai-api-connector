from cryptography.fernet import Fernet
from app.core.config import settings
import base64
import os

# Ensure the key is valid or generate one if it's the default placeholder
KEY_FILE = ".key"

try:
    _key = settings.VAULT_ENCRYPTION_KEY
    if _key == "CHANGE_THIS_TO_A_SECURE_32_BYTE_KEY_BASE64":
        # Check if we have a stored key
        if os.path.exists(KEY_FILE):
            with open(KEY_FILE, "rb") as f:
                _key = f.read()
        else:
            # Generate and save new key
            _key = Fernet.generate_key()
            with open(KEY_FILE, "wb") as f:
                f.write(_key)
    else:
        _key = _key.encode()
    
    cipher_suite = Fernet(_key)
except Exception as e:
    print(f"Warning: Encryption key issue: {e}. Generating a temporary one.")
    _key = Fernet.generate_key()
    cipher_suite = Fernet(_key)

def encrypt(data: str) -> str:
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt(token: str) -> str:
    return cipher_suite.decrypt(token.encode()).decode()
