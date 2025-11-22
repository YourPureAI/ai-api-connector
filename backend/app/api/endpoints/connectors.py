from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Body
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Connector, ConnectorStatus
from app.services.ingestion import parse_openapi_spec, create_connector_from_spec
from app.services.vector_db import process_and_store_connector_chunks
from app.services.vault import vault
from typing import Dict
from . import add_function

router = APIRouter()

# Include add_function routes
router.include_router(add_function.router, tags=["connectors"])

@router.post("/upload")
async def upload_connector(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    content = await file.read()
    spec = parse_openapi_spec(content, file.filename)
    
    # Simulate a user_id for now
    user_id = "demo-user-123"
    
    connector = create_connector_from_spec(spec, user_id, db)
    
    # Trigger background processing (vectorization)
    # In production, use Celery/BackgroundTasks
    process_and_store_connector_chunks(spec, connector.connector_id, user_id)
    
    return {"status": "SUCCESS", "connector_id": connector.connector_id, "auth_type": connector.auth_type}

@router.post("/{connector_id}/secrets")
async def save_secrets(
    connector_id: str,
    secrets: Dict[str, str] = Body(...),
    db: Session = Depends(get_db)
):
    connector = db.query(Connector).filter(Connector.connector_id == connector_id).first()
    if not connector:
        raise HTTPException(status_code=404, detail="Connector not found")
        
    # Simulate user_id
    user_id = "demo-user-123"
    
    vault.store_secrets(user_id, connector_id, secrets)
    
    connector.status = ConnectorStatus.ACTIVE
    db.commit()
    
    return {"status": "SUCCESS", "message": "Secrets saved and connector activated."}

@router.get("/")
def read_connectors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    connectors = db.query(Connector).offset(skip).limit(limit).all()
    return connectors

@router.get("/{connector_id}")
def read_connector(connector_id: str, db: Session = Depends(get_db)):
    connector = db.query(Connector).filter(Connector.connector_id == connector_id).first()
    if not connector:
        raise HTTPException(status_code=404, detail="Connector not found")
    return connector

@router.delete("/{connector_id}")
async def delete_connector(
    connector_id: str,
    db: Session = Depends(get_db)
):
    connector = db.query(Connector).filter(Connector.connector_id == connector_id).first()
    if not connector:
        raise HTTPException(status_code=404, detail="Connector not found")
    
    # Simulate user_id
    user_id = "demo-user-123"
    
    try:
        # 1. Delete from Vector DB
        from app.services.vector_db import vector_db
        vector_db.delete_connector_functions(connector_id)
        
        # 2. Delete from Vault
        vault.delete_secrets(user_id, connector_id)
        
        # 3. Delete from SQL DB
        db.delete(connector)
        db.commit()
        
        return {"status": "SUCCESS", "message": "Connector deleted successfully."}
    except Exception as e:
        print(f"Error deleting connector: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete connector: {str(e)}")
