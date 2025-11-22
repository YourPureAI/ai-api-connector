from fastapi import APIRouter, Depends, HTTPException, Body
from app.services.vault import vault
from typing import Dict, Any

router = APIRouter()

# Use a fixed user/connector ID for global config
SYSTEM_USER_ID = "system"
GLOBAL_CONFIG_ID = "global_config"

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
