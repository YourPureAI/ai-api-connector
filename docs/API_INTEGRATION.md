# API Integration Guide for External Chatbots

This guide explains how external AI chatbots and applications can integrate with the AI API Connector system to query connected APIs using natural language.

---

## Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [Query Endpoint](#query-endpoint)
- [Request Format](#request-format)
- [Response Format](#response-format)
- [Integration Examples](#integration-examples)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

---

## Overview

The AI API Connector provides a RESTful API that allows external chatbots to:
- Send natural language queries
- Automatically match queries to appropriate API functions
- Execute API calls with extracted parameters
- Receive formatted responses

**Base URL:** `http://localhost:8000/api/v1`

**Endpoint:** `POST /query/query`

---

## Authentication

### API Key Authentication

All requests must include an API key in the headers.

**Header:**
```
X-API-Key: your-api-key-here
```

### Getting an API Key

For the demo/test environment, retrieve the test API key:

**Endpoint:** `GET /api/v1/query/test-key`

**Response:**
```json
{
  "api_key": "test-api-key-12345"
}
```

> **Note:** In production, implement proper API key management with user-specific keys.

---

## Query Endpoint

### POST /api/v1/query/query

Send a natural language query to execute API calls through connected connectors.

**URL:** `http://localhost:8000/api/v1/query/query`

**Method:** `POST`

**Headers:**
```
Content-Type: application/json
X-API-Key: test-api-key-12345
```

---

## Request Format

### Basic Request

```json
{
  "query": "Get pet with ID 5",
  "parameters": {}
}
```

### Request Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | Yes | Natural language query describing what you want to do |
| `parameters` | object | No | Optional explicit parameters (usually auto-extracted from query) |

### Examples

**Example 1: Simple Query**
```json
{
  "query": "Show me user with ID 12345"
}
```

**Example 2: Query with Explicit Parameters**
```json
{
  "query": "Get order details",
  "parameters": {
    "orderId": "67890"
  }
}
```

**Example 3: Complex Query**
```json
{
  "query": "List all products with price less than 50"
}
```

---

## Response Format

### Success Response

**Status Code:** `200 OK`

```json
{
  "success": true,
  "data": {
    "id": 5,
    "name": "Fluffy",
    "status": "available",
    "category": {
      "id": 1,
      "name": "Dogs"
    }
  },
  "matched_function": {
    "connector": "Swagger Petstore",
    "operation": "getPetById",
    "path": "/pet/{petId}",
    "method": "get"
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the query was successful |
| `data` | object | The response data from the API call |
| `matched_function` | object | Information about which API function was matched and executed |
| `matched_function.connector` | string | Name of the connector used |
| `matched_function.operation` | string | Operation ID from OpenAPI spec |
| `matched_function.path` | string | API endpoint path |
| `matched_function.method` | string | HTTP method used |

### Error Response

**Status Code:** `200 OK` (with `success: false`)

```json
{
  "success": false,
  "error": "No matching connector function found for this query",
  "matched_function": null
}
```

**Status Code:** `401 Unauthorized`

```json
{
  "detail": "Invalid API key"
}
```

**Status Code:** `500 Internal Server Error`

```json
{
  "detail": "Internal server error message"
}
```

---

## Integration Examples

### Python Example

```python
import requests

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
API_KEY = "test-api-key-12345"

def query_api(natural_language_query):
    """Send a natural language query to the AI API Connector"""
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    
    payload = {
        "query": natural_language_query
    }
    
    response = requests.post(
        f"{BASE_URL}/query/query",
        json=payload,
        headers=headers
    )
    
    if response.status_code == 200:
        result = response.json()
        if result["success"]:
            print(f"✓ Success!")
            print(f"Connector: {result['matched_function']['connector']}")
            print(f"Function: {result['matched_function']['operation']}")
            print(f"Data: {result['data']}")
            return result["data"]
        else:
            print(f"✗ Error: {result['error']}")
            return None
    else:
        print(f"✗ HTTP Error: {response.status_code}")
        return None

# Usage
query_api("Get pet with ID 5")
query_api("Show me order 12345")
```

### JavaScript/Node.js Example

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000/api/v1';
const API_KEY = 'test-api-key-12345';

async function queryAPI(naturalLanguageQuery) {
    try {
        const response = await axios.post(
            `${BASE_URL}/query/query`,
            {
                query: naturalLanguageQuery
            },
            {
                headers: {
                    'Content-Type': 'application/json',
                    'X-API-Key': API_KEY
                }
            }
        );
        
        if (response.data.success) {
            console.log('✓ Success!');
            console.log('Connector:', response.data.matched_function.connector);
            console.log('Function:', response.data.matched_function.operation);
            console.log('Data:', response.data.data);
            return response.data.data;
        } else {
            console.log('✗ Error:', response.data.error);
            return null;
        }
    } catch (error) {
        console.error('✗ Request failed:', error.message);
        return null;
    }
}

// Usage
queryAPI('Get pet with ID 5');
queryAPI('Show me order 12345');
```

### cURL Example

```bash
# Get API key
curl http://localhost:8000/api/v1/query/test-key

# Send query
curl -X POST http://localhost:8000/api/v1/query/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-api-key-12345" \
  -d '{
    "query": "Get pet with ID 5"
  }'
```

---

## Error Handling

### Common Error Scenarios

#### 1. No Matching Function Found

**Response:**
```json
{
  "success": false,
  "error": "No matching connector function found for this query"
}
```

**Cause:** The query doesn't match any configured API functions in the vector database.

**Solution:** 
- Rephrase the query to be more specific
- Ensure the relevant connector is uploaded and configured
- Check that the connector has the required API function

#### 2. Connector Not Active

**Response:**
```json
{
  "success": false,
  "error": "Connector 'Example API' is not active. Please configure authentication secrets first."
}
```

**Cause:** The matched connector hasn't been configured with authentication credentials.

**Solution:** Configure the connector's authentication in the web UI.

#### 3. Invalid Server URL

**Response:**
```json
{
  "success": false,
  "error": "Invalid server URL '/api/v2' in OpenAPI spec. URL must start with 'http://' or 'https://'."
}
```

**Cause:** The OpenAPI specification has an invalid or relative server URL.

**Solution:** Update the OpenAPI spec to include a valid absolute URL.

#### 4. API Execution Failed

**Response:**
```json
{
  "success": false,
  "error": "HTTP 404: Not Found"
}
```

**Cause:** The external API returned an error.

**Solution:** Check the API endpoint, parameters, and authentication.

---

## Best Practices

### 1. Query Formulation

**Good Queries:**
- ✅ "Get user with ID 12345"
- ✅ "List all products"
- ✅ "Create a new order with customer ID 999"
- ✅ "Delete pet with ID 5"

**Poor Queries:**
- ❌ "Show me stuff" (too vague)
- ❌ "API call" (no context)
- ❌ "Data" (no specificity)

### 2. Parameter Extraction

The system automatically extracts parameters from natural language:

**Query:** "Get pet with ID 5"
- Automatically extracts: `petId = 5`

**Query:** "Show order 12345"
- Automatically extracts: `orderId = 12345`

You can also provide explicit parameters:
```json
{
  "query": "Get user details",
  "parameters": {
    "userId": "12345"
  }
}
```

### 3. Error Handling

Always check the `success` field before processing data:

```python
result = query_api("Get pet with ID 5")
if result["success"]:
    # Process data
    data = result["data"]
else:
    # Handle error
    error = result["error"]
```

### 4. Rate Limiting

Implement rate limiting in your chatbot to avoid overwhelming the system:

```python
import time

def rate_limited_query(query, delay=1.0):
    result = query_api(query)
    time.sleep(delay)  # Wait between requests
    return result
```

### 5. Logging

Log all API interactions for debugging:

```python
import logging

logging.info(f"Query: {query}")
logging.info(f"Response: {response}")
```

---

## Advanced Features

### Conversation Context

For multi-turn conversations, maintain context in your chatbot:

```python
conversation_history = []

def query_with_context(query):
    # Add to history
    conversation_history.append({"role": "user", "content": query})
    
    # Send query
    result = query_api(query)
    
    # Add response to history
    if result["success"]:
        conversation_history.append({
            "role": "assistant",
            "content": str(result["data"])
        })
    
    return result
```

### Batch Queries

For multiple related queries:

```python
queries = [
    "Get pet with ID 1",
    "Get pet with ID 2",
    "Get pet with ID 3"
]

results = []
for query in queries:
    result = query_api(query)
    if result["success"]:
        results.append(result["data"])
```

---

## Testing

### Test the Integration

1. **Start the backend:**
   ```bash
   cd backend
   python start.py
   ```

2. **Get the test API key:**
   ```bash
   curl http://localhost:8000/api/v1/query/test-key
   ```

3. **Send a test query:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/query/query \
     -H "Content-Type: application/json" \
     -H "X-API-Key: test-api-key-12345" \
     -d '{"query": "Get pet with ID 5"}'
   ```

4. **Verify the response:**
   - Check `success: true`
   - Verify `data` contains expected information
   - Confirm `matched_function` shows correct connector

---

## API Documentation

For interactive API documentation, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Support

For issues or questions:
- Check the main [README.md](../README.md)
- Review the [Installation Guide](INSTALLATION.md)
- Open an issue on GitHub

---

**Ready to integrate!** Use the examples above to connect your chatbot to the AI API Connector system.
