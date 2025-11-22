# Test script to verify add function endpoint

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Test YAML function definition
yaml_function = """
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
        content:
          application/json:
            schema:
              type: object
"""

# Get first connector
response = requests.get(f"{BASE_URL}/connectors/")
connectors = response.json()

if not connectors:
    print("No connectors found!")
    exit(1)

connector_id = connectors[0]["connector_id"]
print(f"Testing with connector: {connectors[0]['name']} ({connector_id})")

# Add function
print("\nAdding function...")
response = requests.post(
    f"{BASE_URL}/connectors/{connector_id}/add-function",
    json={
        "function_definition": yaml_function,
        "format": "yaml"
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Get updated connector
print("\nFetching updated connector...")
response = requests.get(f"{BASE_URL}/connectors/{connector_id}")
connector = response.json()

print(f"\nTotal paths in connector: {len(connector['full_schema_json']['paths'])}")
print("Paths:")
for path in connector['full_schema_json']['paths'].keys():
    print(f"  - {path}")
