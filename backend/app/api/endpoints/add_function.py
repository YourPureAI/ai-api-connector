from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Connector
from app.services.vector_db import process_and_store_connector_chunks
import yaml
import json
from typing import Literal

router = APIRouter()

class AddFunctionRequest(BaseModel):
    function_definition: str
    format: Literal["yaml", "json"] = "yaml"

@router.post("/{connector_id}/add-function")
async def add_function_to_connector(
    connector_id: str,
    request: AddFunctionRequest,
    db: Session = Depends(get_db)
):
    """
    Add a new function/endpoint to an existing connector.
    
    The function_definition should contain just the path and operation definition,
    not the entire OpenAPI spec.
    
    Example YAML:
    ```yaml
    /pets/{petId}:
      get:
        summary: Get a pet by ID
        operationId: getPetById
        parameters:
          - name: petId
            in: path
            required: true
            schema:
              type: integer
        responses:
          '200':
            description: Success
    ```
    """
    try:
        # Get the connector
        connector = db.query(Connector).filter(Connector.connector_id == connector_id).first()
        if not connector:
            raise HTTPException(status_code=404, detail="Connector not found")
        
        # Parse the function definition
        try:
            if request.format == "yaml":
                new_paths = yaml.safe_load(request.function_definition)
            else:
                new_paths = json.loads(request.function_definition)
        except (yaml.YAMLError, json.JSONDecodeError) as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid {request.format.upper()} format: {str(e)}"
            )
        
        # Validate that it's a path object
        if not isinstance(new_paths, dict):
            raise HTTPException(
                status_code=400,
                detail="Function definition must be a dictionary/object with path(s) as keys"
            )
        
        # Get existing OpenAPI spec
        spec = connector.full_schema_json
        if "paths" not in spec:
            spec["paths"] = {}
        
        # Merge the new paths
        conflicts = []
        for path, methods in new_paths.items():
            if not isinstance(methods, dict):
                raise HTTPException(
                    status_code=400,
                    detail=f"Path '{path}' must contain HTTP methods (get, post, etc.)"
                )
            
            # Check for conflicts
            if path in spec["paths"]:
                for method, operation in methods.items():
                    if method in spec["paths"][path]:
                        conflicts.append(f"{method.upper()} {path}")
            
            # Merge (will overwrite if conflicts exist)
            if path not in spec["paths"]:
                spec["paths"][path] = {}
            
            for method, operation in methods.items():
                # Validate operation has required fields
                if "operationId" not in operation:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Operation {method.upper()} {path} must have an 'operationId'"
                    )
                if "responses" not in operation:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Operation {method.upper()} {path} must have 'responses'"
                    )
                
                spec["paths"][path][method] = operation
        
        # Update the connector in the database
        connector.full_schema_json = spec
        db.commit()
        
        # Re-process the connector to update vector DB
        # Simulate user_id
        user_id = "demo-user-123"
        try:
            process_and_store_connector_chunks(spec, connector.connector_id, user_id)
        except Exception as e:
            # Rollback the database change if vector DB update fails
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update vector database: {str(e)}"
            )
        
        return {
            "status": "SUCCESS",
            "message": f"Added {len(new_paths)} path(s) to connector '{connector.name}'",
            "conflicts": conflicts if conflicts else None,
            "paths_added": list(new_paths.keys())
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
