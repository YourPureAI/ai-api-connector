"""
Test script to verify LLM-based function assessment implementation.

This script tests the assess_function_matches function with various scenarios.
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.llm_service import assess_function_matches


async def test_assessment():
    """Test the function assessment with mock candidates."""
    
    print("=" * 80)
    print("Testing LLM Function Assessment")
    print("=" * 80)
    
    # Test Case 1: Single clear match
    print("\n[TEST 1] Single clear match")
    print("-" * 80)
    query1 = "Get pet with ID 5"
    candidates1 = [
        {
            "metadata": {
                "connector_id": "test-connector-1",
                "operation_id": "getPetById",
                "path": "/pets/{petId}",
                "method": "get"
            },
            "document": "Connector: Pet Store API. Function: getPetById. Path: GET /pets/{petId}. Description: Get a pet by ID",
            "distance": 0.15
        }
    ]
    
    result1 = await assess_function_matches(query1, candidates1)
    print(f"Query: {query1}")
    print(f"Result: {result1}")
    print(f"Expected: selected=True, index=0")
    
    # Test Case 2: Multiple similar functions
    print("\n[TEST 2] Multiple similar functions")
    print("-" * 80)
    query2 = "Show me information about pet 123"
    candidates2 = [
        {
            "metadata": {
                "connector_id": "test-connector-1",
                "operation_id": "getPetById",
                "path": "/pets/{petId}",
                "method": "get"
            },
            "document": "Connector: Pet Store API. Function: getPetById. Path: GET /pets/{petId}. Description: Get a pet by ID",
            "distance": 0.12
        },
        {
            "metadata": {
                "connector_id": "test-connector-1",
                "operation_id": "listPets",
                "path": "/pets",
                "method": "get"
            },
            "document": "Connector: Pet Store API. Function: listPets. Path: GET /pets. Description: List all pets in the store",
            "distance": 0.35
        }
    ]
    
    result2 = await assess_function_matches(query2, candidates2)
    print(f"Query: {query2}")
    print(f"Result: {result2}")
    print(f"Expected: selected=True, index=0 (getPetById)")
    
    # Test Case 3: No matching functions (unrelated query)
    print("\n[TEST 3] No matching functions")
    print("-" * 80)
    query3 = "What's the weather today?"
    candidates3 = [
        {
            "metadata": {
                "connector_id": "test-connector-1",
                "operation_id": "getPetById",
                "path": "/pets/{petId}",
                "method": "get"
            },
            "document": "Connector: Pet Store API. Function: getPetById. Path: GET /pets/{petId}. Description: Get a pet by ID",
            "distance": 0.85
        },
        {
            "metadata": {
                "connector_id": "test-connector-1",
                "operation_id": "listPets",
                "path": "/pets",
                "method": "get"
            },
            "document": "Connector: Pet Store API. Function: listPets. Path: GET /pets. Description: List all pets in the store",
            "distance": 0.92
        }
    ]
    
    result3 = await assess_function_matches(query3, candidates3)
    print(f"Query: {query3}")
    print(f"Result: {result3}")
    print(f"Expected: selected=False, index=None")
    
    # Test Case 4: Empty candidates list
    print("\n[TEST 4] Empty candidates list")
    print("-" * 80)
    query4 = "Get user profile"
    candidates4 = []
    
    result4 = await assess_function_matches(query4, candidates4)
    print(f"Query: {query4}")
    print(f"Result: {result4}")
    print(f"Expected: selected=False, index=None")
    
    print("\n" + "=" * 80)
    print("Testing Complete!")
    print("=" * 80)
    print("\nNOTE: If no LLM is configured, the function will use fallback logic.")
    print("Configure an LLM provider in the global settings to test full functionality.")


if __name__ == "__main__":
    asyncio.run(test_assessment())
