"""
LLM Service for intelligent parameter extraction and query processing.
"""
import json
from typing import Dict, List, Any
from app.services.vault import vault

async def extract_parameters_with_llm(
    query: str,
    param_definitions: List[Dict[str, Any]],
    operation_summary: str = "",
    operation_description: str = ""
) -> Dict[str, Any]:
    """
    Use LLM to intelligently extract parameter values from a natural language query.
    
    Args:
        query: The natural language query from the user
        param_definitions: List of parameter definitions from OpenAPI spec
        operation_summary: Summary of the API operation
        operation_description: Description of the API operation
    
    Returns:
        Dictionary of extracted parameters
    """
    # Get LLM configuration
    config = vault.get_secrets("system", "global_config")
    if not config:
        # Fallback to simple extraction if no LLM configured
        return _fallback_extraction(query, param_definitions)
    
    provider = config.get("agentProvider", "openai")
    model = config.get("agentModel", "gpt-4o")
    
    # Build the prompt for parameter extraction
    prompt = _build_extraction_prompt(query, param_definitions, operation_summary, operation_description)
    
    # Call the appropriate LLM
    try:
        if provider == "openai":
            result = await _call_openai(prompt, model, config.get("openaiApiKey"))
        elif provider == "anthropic":
            result = await _call_anthropic(prompt, model, config.get("anthropicApiKey"))
        elif provider == "google":
            result = await _call_google(prompt, model, config.get("googleApiKey"))
        else:
            return _fallback_extraction(query, param_definitions)
        
        # Parse the LLM response
        return _parse_llm_response(result, param_definitions)
    
    except Exception as e:
        print(f"LLM extraction failed: {e}, falling back to regex")
        return _fallback_extraction(query, param_definitions)


def _build_extraction_prompt(
    query: str,
    param_definitions: List[Dict[str, Any]],
    operation_summary: str,
    operation_description: str
) -> str:
    """Build a prompt for the LLM to extract parameters."""
    
    # Format parameter definitions
    params_info = []
    for param in param_definitions:
        param_name = param.get("name", "")
        param_in = param.get("in", "")
        param_type = param.get("schema", {}).get("type", "string")
        param_desc = param.get("description", "")
        required = param.get("required", False)
        
        params_info.append(
            f"- {param_name} ({param_in}, {param_type}): {param_desc} {'[REQUIRED]' if required else '[OPTIONAL]'}"
        )
    
    params_text = "\n".join(params_info)
    
    prompt = f"""You are a parameter extraction assistant. Extract parameter values from a natural language query for an API call.

API Operation: {operation_summary or operation_description or "API call"}

Parameters to extract:
{params_text}

User Query: "{query}"

Extract the parameter values from the query and return them as a JSON object. Only include parameters that you can confidently extract from the query.

Rules:
1. Match parameter values based on context and meaning, not just keywords
2. Convert values to the correct type (numbers for integer/number types, strings for string types)
3. If a parameter cannot be determined from the query, omit it from the response
4. Return ONLY valid JSON, no explanations

Example format:
{{"parameterName": "value", "anotherId": 123}}

Response:"""
    
    return prompt


async def _call_openai(prompt: str, model: str, api_key: str) -> str:
    """Call OpenAI API for parameter extraction."""
    import httpx
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that extracts parameters from natural language queries. Always respond with valid JSON only."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 200
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]


async def _call_anthropic(prompt: str, model: str, api_key: str) -> str:
    """Call Anthropic API for parameter extraction."""
    import httpx
    
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "max_tokens": 200,
        "temperature": 0.1,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        return result["content"][0]["text"]


async def _call_google(prompt: str, model: str, api_key: str) -> str:
    """Call Google Gemini API for parameter extraction."""
    import httpx
    
    # Strip 'models/' prefix if present
    if model.startswith("models/"):
        model = model[7:]
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 200
        }
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]


def _parse_llm_response(response: str, param_definitions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Parse the LLM response and extract parameters."""
    try:
        # Try to extract JSON from the response
        # Sometimes LLMs wrap JSON in markdown code blocks
        response = response.strip()
        
        # Remove markdown code blocks if present
        if response.startswith("```"):
            lines = response.split("\n")
            response = "\n".join(lines[1:-1]) if len(lines) > 2 else response
            response = response.replace("```json", "").replace("```", "").strip()
        
        # Parse JSON
        params = json.loads(response)
        
        # Validate and convert types based on parameter definitions
        validated_params = {}
        for param_def in param_definitions:
            param_name = param_def.get("name")
            if param_name in params:
                param_type = param_def.get("schema", {}).get("type", "string")
                value = params[param_name]
                
                # Convert to correct type
                if param_type == "integer":
                    validated_params[param_name] = int(value)
                elif param_type == "number":
                    validated_params[param_name] = float(value)
                elif param_type == "boolean":
                    validated_params[param_name] = bool(value)
                else:
                    validated_params[param_name] = str(value)
        
        return validated_params
    
    except Exception as e:
        print(f"Failed to parse LLM response: {e}")
        print(f"Response was: {response}")
        return {}


def _fallback_extraction(query: str, param_definitions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Fallback regex-based parameter extraction."""
    import re
    
    params = {}
    query_lower = query.lower()
    
    for param_def in param_definitions:
        param_name = param_def.get("name", "")
        param_type = param_def.get("schema", {}).get("type", "string")
        
        # Try to find the parameter value
        param_lower = param_name.lower()
        
        # Look for "param value" pattern
        pattern = rf'\b{param_lower}[:\s]+(\w+)'
        match = re.search(pattern, query_lower)
        
        if match:
            value = match.group(1)
            if param_type == "integer":
                try:
                    params[param_name] = int(value)
                except:
                    pass
            else:
                params[param_name] = value
        else:
            # Try to find any number for integer/number types
            if param_type in ["integer", "number"]:
                numbers = re.findall(r'\b\d+\b', query)
                if numbers:
                    params[param_name] = int(numbers[-1]) if param_type == "integer" else float(numbers[-1])
    
    return params
