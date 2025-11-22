from fastapi import APIRouter, Depends, HTTPException, Body
from app.services.vault import vault
from typing import Dict, Any
import secrets
import string

router = APIRouter()

# Use a fixed user/connector ID for global config
SYSTEM_USER_ID = "system"
GLOBAL_CONFIG_ID = "global_config"
API_KEY_CONFIG_ID = "api_keys"

def generate_api_key(length=32):
    """Generate a secure random API key"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

@router.get("/")
async def get_config():
    """Retrieve the system configuration from the vault."""
    config = vault.get_secrets(SYSTEM_USER_ID, GLOBAL_CONFIG_ID)
    # If no config exists, return empty defaults (or could return 404, but empty is better for UI)
    if not config:
        return {
            "agentProvider": "openai",
            "agentModel": "gpt-4o",
            "embeddingProvider": "openai",
            "embeddingModel": "text-embedding-3-small",
            "logLevel": "INFO",
            "openaiApiKey": "",
            "anthropicApiKey": "",
            "googleApiKey": ""
        }
    return config

@router.post("/")
async def save_config(config: Dict[str, Any] = Body(...)):
    """Save the system configuration to the vault."""
    vault.store_secrets(SYSTEM_USER_ID, GLOBAL_CONFIG_ID, config)
    return {"status": "SUCCESS", "message": "Configuration saved securely."}

@router.get("/api-key")
async def get_api_key():
    """Get the current API key for external integrations"""
    api_keys = vault.get_secrets(SYSTEM_USER_ID, API_KEY_CONFIG_ID)
    
    if not api_keys or "current_key" not in api_keys:
        # Generate initial API key if none exists
        new_key = generate_api_key()
        vault.store_secrets(SYSTEM_USER_ID, API_KEY_CONFIG_ID, {
            "current_key": new_key,
            "keys": [new_key]
        })
        return {
            "api_key": new_key,
            "created": True
        }
    
    return {
        "api_key": api_keys["current_key"],
        "created": False
    }

@router.post("/api-key/regenerate")
async def regenerate_api_key():
    """Generate a new API key (invalidates the old one)"""
    new_key = generate_api_key()
    
    # Get existing keys
    api_keys = vault.get_secrets(SYSTEM_USER_ID, API_KEY_CONFIG_ID)
    
    if not api_keys:
        api_keys = {"keys": []}
    
    # Store new key
    api_keys["current_key"] = new_key
    if "keys" not in api_keys:
        api_keys["keys"] = []
    api_keys["keys"].append(new_key)
    
    # Keep only last 5 keys for history
    if len(api_keys["keys"]) > 5:
        api_keys["keys"] = api_keys["keys"][-5:]
    
    vault.store_secrets(SYSTEM_USER_ID, API_KEY_CONFIG_ID, api_keys)
    
    return {
        "status": "SUCCESS",
        "api_key": new_key,
        "message": "New API key generated successfully"
    }
