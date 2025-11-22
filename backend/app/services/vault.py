import os
import json
from app.core.config import settings
from app.core.security import encrypt, decrypt

class LocalVault:
    def __init__(self):
        self.vault_path = settings.VAULT_PATH
        if not os.path.exists(self.vault_path):
            os.makedirs(self.vault_path)

    def _get_path(self, user_id: str, connector_id: str) -> str:
        user_path = os.path.join(self.vault_path, user_id)
        if not os.path.exists(user_path):
            os.makedirs(user_path)
        return os.path.join(user_path, f"{connector_id}.enc")

    def store_secrets(self, user_id: str, connector_id: str, secrets: dict):
        file_path = self._get_path(user_id, connector_id)
        json_data = json.dumps(secrets)
        encrypted_data = encrypt(json_data)
        
        with open(file_path, "w") as f:
            f.write(encrypted_data)

    def get_secrets(self, user_id: str, connector_id: str) -> dict:
        file_path = self._get_path(user_id, connector_id)
        if not os.path.exists(file_path):
            return {}
            
        with open(file_path, "r") as f:
            encrypted_data = f.read()
            
        try:
            json_data = decrypt(encrypted_data)
            return json.loads(json_data)
        except Exception:
            return {}

    def delete_secrets(self, user_id: str, connector_id: str):
        file_path = self._get_path(user_id, connector_id)
        if os.path.exists(file_path):
            os.remove(file_path)

vault = LocalVault()
