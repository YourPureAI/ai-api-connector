from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI API Connector"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "CHANGE_THIS_TO_A_SECURE_RANDOM_KEY" # In production, get from env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./sql_app.db"
    
    # Vector DB
    CHROMA_DB_PATH: str = "./chroma_db"
    
    # Vault
    VAULT_PATH: str = "./vault"
    VAULT_ENCRYPTION_KEY: str = "CHANGE_THIS_TO_A_SECURE_32_BYTE_KEY_BASE64" # In production, get from env

    # AI
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()
