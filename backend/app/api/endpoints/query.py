from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Connector
from app.services.vector_db import vector_db
from app.services.executor import executor
import re

router = APIRouter()

# Simple API key for demo purposes
DEMO_API_KEY = "test-api-key-12345"

class QueryRequest(BaseModel):
    query: str
    parameters: Optional[dict] = None

class QueryResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None
    matched_function: Optional[dict] = None

def verify_api_key(x_api_key: str = Header(...)):
    """Simple API key verification for the test chatbot."""
    if x_api_key != DEMO_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@router.post("/query", response_model=QueryResponse)
async def query_data(
    request: QueryRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    Main endpoint for external chatbot to query data through our connectors.
    
    This endpoint:
    1. Receives a natural language query
    2. Searches the vector DB for matching connector functions
    3. Executes the API call to the external service
    4. Returns the data to the chatbot
    """
    try:
        # Search vector DB for matching functions using configured embedding model
        results = vector_db.search_functions(request.query, n_results=1)
        
        if not results or not results.get("ids") or len(results["ids"][0]) == 0:
            return QueryResponse(
                success=False,
                error="No matching connector function found for this query"
            )
        
        # Get the best match
        metadata = results["metadatas"][0][0]
        connector_id = metadata["connector_id"]
        operation_id = metadata["operation_id"]
        path = metadata["path"]
        method = metadata["method"]
        
        # Get connector from database
        connector = db.query(Connector).filter(Connector.connector_id == connector_id).first()
        if not connector:
            return QueryResponse(
                success=False,
                error="Connector not found in database"
            )
        
        # Check if connector has secrets configured
        if connector.status != "ACTIVE":
            return QueryResponse(
                success=False,
                error=f"Connector '{connector.name}' is not active. Please configure authentication secrets first."
            )
        
        # Extract parameters from the query if needed
        parameters = request.parameters or {}
        
        print(f"[QUERY] User query: {request.query}")
        print(f"[QUERY] Matched path: {path}")
        print(f"[QUERY] Matched method: {method}")
        
        # If path has parameters, use LLM to extract them intelligently
        if "{" in path and "}" in path:
            print(f"[QUERY] Path contains parameters, attempting extraction...")
            
            # Get the operation details from the OpenAPI spec
            spec = connector.full_schema_json
            operation_spec = spec.get("paths", {}).get(path, {}).get(method.lower(), {})
            
            # Get parameter definitions
            param_definitions = operation_spec.get("parameters", [])
            
            print(f"[QUERY] Found {len(param_definitions)} parameter definitions")
            
            if param_definitions:
                # Use LLM to extract parameters
                from app.services.llm_service import extract_parameters_with_llm
                
                print(f"[QUERY] Calling LLM for parameter extraction...")
                try:
                    extracted_params = await extract_parameters_with_llm(
                        query=request.query,
                        param_definitions=param_definitions,
                        operation_summary=operation_spec.get("summary", ""),
                        operation_description=operation_spec.get("description", "")
                    )
                    print(f"[QUERY] LLM extracted parameters: {extracted_params}")
                except Exception as e:
                    print(f"[QUERY] LLM extraction failed: {e}")
                    import traceback
                    traceback.print_exc()
                    extracted_params = {}
                
                # Merge extracted parameters with any explicitly provided ones
                parameters = {**extracted_params, **parameters}
            else:
                print(f"[QUERY] No parameter definitions, using fallback regex extraction")
                # Fallback to regex-based extraction if no parameter definitions
                path_params = re.findall(r'\{(\w+)\}', path)
                query_lower = request.query.lower()
                
                for param in path_params:
                    if param not in parameters:
                        # Try to find numbers in the query
                        numbers = re.findall(r'\b\d+\b', request.query)
                        if numbers:
                            parameters[param] = numbers[-1]
                            print(f"[QUERY] Regex extracted {param} = {numbers[-1]}")
        
        print(f"[QUERY] Final parameters to pass to executor: {parameters}")
        
        # Execute the API call
        user_id = "demo-user-123"  # Demo user ID
        result = await executor.execute_function(
            connector=connector,
            operation_id=operation_id,
            path=path,
            method=method,
            user_id=user_id,
            parameters=parameters
        )
        
        if result.get("success"):
            return QueryResponse(
                success=True,
                data=result.get("data"),
                matched_function={
                    "connector": connector.name,
                    "operation": operation_id,
                    "path": path,
                    "method": method
                }
            )
        else:
            return QueryResponse(
                success=False,
                error=result.get("error"),
                matched_function={
                    "connector": connector.name,
                    "operation": operation_id,
                    "path": path,
                    "method": method
                }
            )
            
    except Exception as e:
        print(f"[QUERY] Exception occurred: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test-key")
def get_test_api_key():
    """Returns the test API key for the demo chatbot."""
    return {"api_key": DEMO_API_KEY}
