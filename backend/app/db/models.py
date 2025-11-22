from sqlalchemy import Column, String, Enum, DateTime, Text
from sqlalchemy.dialects.sqlite import JSON
from app.db.session import Base
import uuid
import datetime
import enum

class ConnectorStatus(str, enum.Enum):
    PENDING_SECRETS = "PENDING_SECRETS"
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"

class Connector(Base):
    __tablename__ = "connectors"

    connector_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True, nullable=False) # For now, we can simulate user_id
    name = Column(String, nullable=False)
    description = Column(String)
    version = Column(String)
    auth_type = Column(String, nullable=False)
    full_schema_json = Column(JSON, nullable=False)
    status = Column(Enum(ConnectorStatus), default=ConnectorStatus.PENDING_SECRETS)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
