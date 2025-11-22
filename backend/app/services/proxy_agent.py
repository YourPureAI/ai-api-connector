from typing import Dict, Any, Optional
from app.services.vector_db import vector_db
from app.services.vault import vault
from app.db.session import SessionLocal
from app.db.models import Connector
import httpx
import json

class ProxyAgent:
    def __init__(self):
        pass

    async def process_query(self, user_query: str, conversation_id: str, user_context_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # 1. Analysis (Simplified for demo: Check if context data exists)
        # In a real system, we would use an LLM here to decide.
        
        if user_context_data:
            # B) Execution with data
            # For demo purposes, we assume the query implies an action on the data.
            # We search for a tool that matches the query AND can handle the data.
            print(f"Processing execution request with context: {user_context_data}")
            pass
        else:
            # A) Search
            print(f"Processing search request: {user_query}")
            results = vector_db.search_functions(user_query, n_results=1)
            
            if not results['documents'][0]:
                return {
                    "status": "FAILURE",
                    "error_code": "NO_TOOL_FOUND",
                    "error_message": "No relevant tool found for your query."
                }
                
            metadata = results['metadatas'][0][0]
            connector_id = metadata['connector_id']
            operation_id = metadata['operation_id']
            
            # Fetch connector details to get the host URL
            db = SessionLocal()
            connector = db.query(Connector).filter(Connector.connector_id == connector_id).first()
            if not connector:
                db.close()
                return {"status": "FAILURE", "error_message": "Connector not found."}
                
            # Get secrets
            secrets = vault.get_secrets(connector.user_id, connector_id)
            
            # Mock Execution (since we don't have a real API to call in this demo environment usually)
            # In a real app, we would construct the HTTP request based on the OpenAPI spec and secrets.
            
            response_data = {
                "status": "SUCCESS",
                "final_data": {
                    "message": f"Executed {operation_id} on {connector.name}",
                    "result": "Mock Data Result"
                }
            }
            db.close()
            return response_data

        return {"status": "SUCCESS", "final_data": {"message": "Action processed"}}

proxy_agent = ProxyAgent()
