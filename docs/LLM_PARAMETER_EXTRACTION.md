# LLM-Based Parameter Extraction

## Overview

The AI API Connector now uses **intelligent LLM-based parameter extraction** to accurately extract parameter values from natural language queries.

## How It Works

### 1. **Query Processing Flow**

```
User Query → Vector DB Search → Match Function → Extract Parameters (LLM) → Execute API Call
```

### 2. **LLM Parameter Extraction**

When a query like `"get store id 4 noobstory"` is received:

1. **Retrieve Parameter Definitions** from the OpenAPI spec:
   ```json
   {
     "name": "orderId",
     "in": "path",
     "required": true,
     "schema": {"type": "integer"},
     "description": "ID of the order to retrieve"
   }
   ```

2. **Build Intelligent Prompt** for the LLM:
   ```
   Extract parameter values from: "get store id 4 noobstory"
   
   Parameters needed:
   - orderId (path, integer): ID of the order to retrieve [REQUIRED]
   
   Return JSON with extracted values.
   ```

3. **LLM Analyzes Context** and returns:
   ```json
   {"orderId": 4}
   ```

4. **Replace Path Parameters**:
   - Original: `/store/order/{orderId}`
   - Final: `/store/order/4`

### 3. **Multi-Provider Support**

The system uses the configured LLM provider from Configuration:
- **OpenAI** (GPT-4, GPT-3.5)
- **Anthropic** (Claude)
- **Google** (Gemini)

### 4. **Fallback Mechanism**

If LLM extraction fails or is unavailable:
- Falls back to regex-based extraction
- Looks for numbers and common patterns
- Ensures the system always works

## Advantages Over Regex

| Feature | Regex | LLM |
|---------|-------|-----|
| **Context Understanding** | ❌ No | ✅ Yes |
| **Multiple Parameters** | ⚠️ Limited | ✅ Excellent |
| **Ambiguous Queries** | ❌ Fails | ✅ Handles well |
| **Type Conversion** | ⚠️ Manual | ✅ Automatic |
| **Natural Language** | ❌ Rigid | ✅ Flexible |

## Examples

### Example 1: Simple ID Extraction
**Query**: `"get order 123"`
- **Regex**: Might extract `123` for any parameter
- **LLM**: Understands `123` is the `orderId` based on context

### Example 2: Multiple Parameters
**Query**: `"find user john with age 25"`
- **Regex**: Struggles with multiple values
- **LLM**: Correctly maps `john` → `username`, `25` → `age`

### Example 3: Ambiguous Values
**Query**: `"get store id 4 noobstory"`
- **Regex**: Might confuse `4` and `noobstory`
- **LLM**: Knows `4` is numeric ID, ignores `noobstory`

### Example 4: Natural Phrasing
**Query**: `"show me details for pet number 42"`
- **Regex**: Might miss "number 42" pattern
- **LLM**: Understands intent and extracts `42` for `petId`

## Configuration

The LLM service automatically uses the provider configured in **Configuration** page:
- Agent Provider: OpenAI/Anthropic/Google
- Agent Model: gpt-4o, claude-3-5-sonnet, gemini-2.5-flash, etc.
- API Keys: Securely stored in vault

## Code Location

- **LLM Service**: `backend/app/services/llm_service.py`
- **Query Endpoint**: `backend/app/api/endpoints/query.py`
- **Executor**: `backend/app/services/executor.py`

## Benefits

1. ✅ **Accurate**: Understands context and meaning
2. ✅ **Flexible**: Handles various natural language phrasings
3. ✅ **Type-Safe**: Automatically converts to correct types
4. ✅ **Robust**: Fallback to regex if LLM unavailable
5. ✅ **Scalable**: Works with any number of parameters
