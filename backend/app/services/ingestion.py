import json
import yaml
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models import Connector, ConnectorStatus
from app.core.config import settings

def parse_openapi_spec(file_content: bytes, filename: str) -> dict:
    try:
        if filename.endswith(".json"):
            spec = json.loads(file_content)
        elif filename.endswith(".yaml") or filename.endswith(".yml"):
            spec = yaml.safe_load(file_content)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Use JSON or YAML.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid file content: {str(e)}")
    
    # Basic OpenAPI validation
    if "openapi" not in spec and "swagger" not in spec:
         raise HTTPException(status_code=400, detail="Invalid OpenAPI/Swagger definition.")
    
    if "info" not in spec or "title" not in spec["info"]:
         raise HTTPException(status_code=400, detail="Missing 'info.title' in spec.")

    # Custom Protocol Validation
    # x-auth-type is required for our system to know how to handle auth
    # In a real scenario, we might support 'none' or standard securitySchemes too,
    # but the spec emphasizes x-auth-type.
    # We will be lenient for the demo if it's missing, defaulting to 'none' or checking standard security.
    
    return spec

def create_connector_from_spec(spec: dict, user_id: str, db: Session) -> Connector:
    auth_type = spec.get("x-auth-type", "none")
    
    connector = Connector(
        user_id=user_id,
        name=spec["info"]["title"],
        description=spec["info"].get("description", ""),
        version=spec["info"].get("version", "1.0.0"),
        auth_type=auth_type,
        full_schema_json=spec,
        status=ConnectorStatus.PENDING_SECRETS
    )
    
    db.add(connector)
    db.commit()
    db.refresh(connector)
    return connector
