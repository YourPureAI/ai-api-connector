import httpx
from typing import Dict, Any, Optional
import json
from app.db.models import Connector
from app.services.vault import vault
from sqlalchemy.orm import Session

class APIExecutor:
    """
    Service to execute API calls to external services based on OpenAPI specs.
    """
    
    async def execute_function(
        self,
        connector: Connector,
        operation_id: str,
        path: str,
        method: str,
        user_id: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute an API call to an external service.
        
        Args:
            connector: The connector object with OpenAPI spec
            operation_id: The operation ID from the spec
            path: The API path
            method: HTTP method (get, post, etc.)
            user_id: User ID for retrieving credentials
            parameters: Optional parameters for the API call
            
        Returns:
            Dict with response data or error
        """
        try:
            # Get the full OpenAPI spec
            spec = connector.full_schema_json
            
            # Get base URL from servers
            servers = spec.get("servers", [])
            if not servers or len(servers) == 0:
                return {
                    "success": False,
                    "error": f"No server URL defined in the OpenAPI spec for connector '{connector.name}'. Please update the spec to include a 'servers' section with a valid base URL."
                }
            
            base_url = servers[0].get("url", "")
            if not base_url:
                return {
                    "success": False,
                    "error": f"Server URL is empty in the OpenAPI spec for connector '{connector.name}'."
                }
            
            # Ensure base_url has a protocol
            if not base_url.startswith(('http://', 'https://')):
                # If it's a relative URL, we can't use it without a host
                return {
                    "success": False,
                    "error": f"Invalid server URL '{base_url}' in OpenAPI spec. URL must start with 'http://' or 'https://'. Please update the connector's OpenAPI specification."
                }
            
            # Get credentials from vault
            secrets = vault.get_secrets(user_id, connector.connector_id)
            
            # Build headers
            headers = {"Content-Type": "application/json"}
            
            # Add authentication based on spec
            auth_type = spec.get("x-auth-type", "api-key")
            if auth_type == "api-key":
                api_key = secrets.get("api_key")
                if api_key:
                    # Check if spec defines where to put the API key
                    security_schemes = spec.get("components", {}).get("securitySchemes", {})
                    if security_schemes:
                        # Use the first security scheme
                        scheme = list(security_schemes.values())[0]
                        if scheme.get("in") == "header":
                            key_name = scheme.get("name", "Authorization")
                            headers[key_name] = f"Bearer {api_key}" if "Authorization" in key_name else api_key
                    else:
                        # Default to Authorization header
                        headers["Authorization"] = f"Bearer {api_key}"
            
            # Build full URL
            full_url = f"{base_url.rstrip('/')}{path}"
            
            # Replace path parameters if any
            if parameters:
                for key, value in parameters.items():
                    full_url = full_url.replace(f"{{{key}}}", str(value))
            
            # Make the request
            async with httpx.AsyncClient(timeout=30.0) as client:
                if method.lower() == "get":
                    response = await client.get(full_url, headers=headers)
                elif method.lower() == "post":
                    response = await client.post(full_url, headers=headers, json=parameters or {})
                elif method.lower() == "put":
                    response = await client.put(full_url, headers=headers, json=parameters or {})
                elif method.lower() == "delete":
                    response = await client.delete(full_url, headers=headers)
                else:
                    return {"error": f"Unsupported HTTP method: {method}"}
                
                # Parse response
                response.raise_for_status()
                
                try:
                    data = response.json()
                except:
                    data = {"response": response.text}
                
                return {
                    "success": True,
                    "data": data,
                    "status_code": response.status_code
                }
                
        except httpx.HTTPStatusError as e:
            return {
                "success": False,
                "error": f"HTTP {e.response.status_code}: {e.response.text}",
                "status_code": e.response.status_code
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

executor = APIExecutor()
